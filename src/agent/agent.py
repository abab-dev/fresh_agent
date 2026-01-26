from typing import Protocol, Optional, TYPE_CHECKING, List, Dict, Any, Callable

from src.agent.client import LLMClient
from src.agent.message import MessageBuilder
from src.agent.response import ResponseHandler
from src.agent.executor import ToolExecutor
from src.subagents.runner import SubagentRunner

if TYPE_CHECKING:
    from src.tools.manager import ToolManager
    from src.history.manager import HistoryManager
    from src.prompts.manager import PromptManager
    from src.subagents.manager import SubagentManager


class UIProtocol(Protocol):
    def print_simple_message(self, message: str, prefix: str = "") -> None: ...
    def print_info(self, message: str) -> None: ...
    def print_assistant_message(self, message: str) -> None: ...
    async def get_user_input(self) -> str: ...
    def start_stream_display(self) -> None: ...
    def print_streaming_content(self, content: str) -> None: ...
    def stop_stream_display(self) -> None: ...
    def show_preparing_tool(self, name: str, args: dict) -> None: ...
    def show_tool_execution(self, name: str, args: dict, success: bool, result: str) -> None: ...
    async def wait_for_user_approval(self, content: str) -> tuple: ...


class Agent:
    
    def __init__(
        self,
        tool_manager: "ToolManager",
        api_client: LLMClient,
        ui_manager: UIProtocol,
        history_manager: "HistoryManager",
        prompt_manager: "PromptManager",
        subagent_manager: Optional["SubagentManager"] = None,
        is_headless: bool = False
    ):
        self._tool_manager = tool_manager
        self._api_client = api_client
        self._ui_manager = ui_manager
        self._history_manager = history_manager
        self._prompt_manager = prompt_manager
        self._subagent_manager = subagent_manager
        self._is_in_task = False
        self._is_headless = is_headless
        self._on_turn_complete: Optional[Callable] = None
        
        self._response_handler = ResponseHandler(ui_manager)
        
        # Create sub-agent runner if manager is available
        subagent_runner = None
        if subagent_manager:
            subagent_runner = SubagentRunner(
                llm_client=api_client,
                tool_manager=tool_manager,
                subagent_manager=subagent_manager
            )
        
        self._tool_executor = ToolExecutor(
            tool_manager, 
            ui_manager, 
            self.add_message,
            subagent_runner=subagent_runner
        )

    @property
    def messages(self) -> List[Dict[str, Any]]:
        """Get all messages in the conversation."""
        return self._history_manager.get_current_messages()
    
    @property
    def session_id(self) -> Optional[str]:
        """Get the current session ID (from HistoryManager)."""
        return getattr(self._history_manager, 'session_id', None)
    
    @property
    def total_cost(self) -> float:
        """Get total API cost for this session."""
        return self._api_client.total_cost
    
    def add_message(self, message: Dict[str, Any]) -> None:
        """Add a message to the conversation history."""
        self._history_manager.add_message(message)

    async def start_conversation(
        self, 
        on_turn_complete: Optional[Callable] = None
    ) -> None:
        """
        Start the main conversation loop.
        
        Args:
            on_turn_complete: Optional async callback called after each turn completes.
                              Use for saving session state.
        """
        self._on_turn_complete = on_turn_complete
        
        # Only add system message if not resuming (no existing messages)
        if not self.messages:
            self.add_message(
                MessageBuilder.create_system_message(
                    self._prompt_manager.get_system_prompt()
                )
            )
        
        user_input = await self._ui_manager.get_user_input()
        self.add_message(MessageBuilder.create_user_message(user_input))

        await self._recursive_message_handling()

    async def start_task(self, task_system_prompt: str, user_input: str) -> str:
        self._is_in_task = True
        self._history_manager.start_new_chat()
        
        self.add_message(MessageBuilder.create_system_message(task_system_prompt))
        self.add_message(MessageBuilder.create_user_message(user_input))

        await self._recursive_message_handling()
        self._is_in_task = False
        return self._history_manager.finish_chat_get_response()

    async def _recursive_message_handling(self):
        self._history_manager.auto_messages_compression()

        request = self._build_api_request()
        
        self._ui_manager.print_simple_message("", "🤖")
        
        stream_generator = self._api_client.get_completion_stream(request)
        
        if stream_generator is None:
            raise Exception("Stream generator is None - API client returned no response")
        
        response_message, _, token_usage = self._response_handler.process_stream(
            stream_generator
        )
            
        if token_usage:
            self._history_manager.update_token_usage(token_usage)
        
        assistant_message = self._build_assistant_message(response_message)
        self.add_message(assistant_message)
        
        self._history_manager.auto_messages_compression()

        if ResponseHandler.has_tool_calls(response_message) and len(response_message.tool_calls) > 0:
            get_reminders = getattr(self._prompt_manager, 'get_reminders', None)
            await self._tool_executor.handle_tool_calls(response_message.tool_calls, get_reminders)
            self._print_context_window_and_total_cost()
            await self._recursive_message_handling()
        else:
            self._print_context_window_and_total_cost()
            await self._handle_conversation_turn(response_message)

    def _build_api_request(self) -> dict:
        messages = MessageBuilder.apply_cache_control(
            self._history_manager.get_current_messages()
        )
        # Sanitize messages - Gemini requires non-empty content
        messages = self._sanitize_messages(messages)
        return {
            "messages": messages,
            # Use main agent tools (excludes explorer-only search tools)
            "tools": self._tool_manager.get_main_agent_tools(),
        }
    
    def _sanitize_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ensure all messages have valid content for Gemini API."""
        for msg in messages:
            if msg.get("role") == "assistant":
                content = msg.get("content", "")
                # Empty string or None is invalid - add placeholder
                if not content or (isinstance(content, str) and not content.strip()):
                    msg["content"] = "."
        return messages

    def _build_assistant_message(self, response_message) -> dict:
        has_tool_calls = ResponseHandler.has_tool_calls(response_message)
        content = response_message.content or ""
        trimmed_content = ResponseHandler.get_trimmed_content(content)
        
        assistant_message = MessageBuilder.create_assistant_message(
            content=response_message.content if response_message.content else None,
            tool_calls=response_message.tool_calls if has_tool_calls else None
        )
        
        # Gemini API requires non-empty text in content
        # If no text content, add a minimal placeholder
        if not trimmed_content:
            if has_tool_calls:
                # Tool-only turn - add minimal placeholder
                assistant_message["content"] = "."
            else:
                self._ui_manager.print_info(
                    "[debug] Assistant returned empty response, using fallback message"
                )
                assistant_message["content"] = MessageBuilder.create_fallback_content()
        
        return assistant_message

    async def _handle_conversation_turn(self, response_message):
        has_tool_calls = ResponseHandler.has_tool_calls(response_message)
        content = response_message.content or ""
        trimmed_content = ResponseHandler.get_trimmed_content(content)
        
        if self._is_in_task or self._is_headless:
            if not has_tool_calls:
                self._ui_manager.print_info(
                    f"[debug] Turn completed without tool call | len={len(trimmed_content)}"
                )
            return
        
        # Save session after each turn
        if self._on_turn_complete:
            await self._on_turn_complete()
        
        user_input = await self._ui_manager.get_user_input()
        self.add_message(MessageBuilder.create_user_message(user_input))
        await self._recursive_message_handling()

    def _print_context_window_and_total_cost(self):
        self._ui_manager.print_simple_message(
            f"(context window: {self._history_manager.current_context_window}%, "
            f"total cost: ${self._api_client.total_cost})"
        )
