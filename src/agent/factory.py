from typing import Optional, TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from src.tools.manager import ToolManager
    from src.history.manager import HistoryManager
    from src.agent.client import LLMClient
    from src.agent.config import AgentConfig
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


class AgentFactory:
    @staticmethod
    def create_tool_manager(
        history_manager: Optional["HistoryManager"] = None,
        ui_manager: Optional[UIProtocol] = None,
        subagent_manager: Optional["SubagentManager"] = None
    ) -> "ToolManager":
        from src.tools.manager import ToolManager
        return ToolManager(
            history_manager=history_manager,
            ui_manager=ui_manager,
            subagent_manager=subagent_manager
        )
    
    @staticmethod
    def create_api_client(config: Optional["AgentConfig"] = None) -> "LLMClient":
        from src.agent.client import LLMClient
        return LLMClient(config=config)
    
    @staticmethod
    def create_prompt_manager() -> "PromptManager":
        from src.prompts.manager import PromptManager
        return PromptManager()
    
    @staticmethod
    def create_subagent_manager() -> "SubagentManager":
        from src.subagents.manager import SubagentManager
        return SubagentManager()
    
    @staticmethod
    def create_history_manager(
        ui_manager: Optional[UIProtocol] = None,
        api_client: Optional["LLMClient"] = None,
        model_max_tokens: int = 200,
        compress_threshold: float = 0.8
    ) -> "HistoryManager":
        from src.history.manager import HistoryManager
        if ui_manager is None:
            raise ValueError("ui_manager must be provided for HistoryManager.")
        return HistoryManager(
            ui_manager=ui_manager,
            api_client=api_client,
            model_max_tokens=model_max_tokens,
            compress_threshold=compress_threshold
        )
    
    @staticmethod
    def create_agent(
        tool_manager: Optional["ToolManager"] = None,
        api_client: Optional["LLMClient"] = None,
        ui_manager: Optional[UIProtocol] = None,
        history_manager: Optional["HistoryManager"] = None,
        prompt_manager: Optional["PromptManager"] = None,
        subagent_manager: Optional["SubagentManager"] = None,
        is_headless: bool = False
    ):
        from src.agent.agent import Agent
        
        if ui_manager is None:
            raise ValueError("ui_manager must be provided. No default implementation available.")
        
        if api_client is None:
            api_client = AgentFactory.create_api_client()
            
        if history_manager is None:
            history_manager = AgentFactory.create_history_manager(
                ui_manager=ui_manager,
                api_client=api_client
            )
            
        if tool_manager is None:
            tool_manager = AgentFactory.create_tool_manager(
                history_manager=history_manager,
                ui_manager=ui_manager,
                subagent_manager=subagent_manager
            )
            
        if prompt_manager is None:
            prompt_manager = AgentFactory.create_prompt_manager()

        if subagent_manager is None:
            subagent_manager = AgentFactory.create_subagent_manager()
        
        return Agent(
            tool_manager=tool_manager,
            api_client=api_client,
            ui_manager=ui_manager,
            history_manager=history_manager,
            prompt_manager=prompt_manager,
            subagent_manager=subagent_manager,
            is_headless=is_headless
        )
