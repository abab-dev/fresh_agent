"""
Tool executor with delegation support.

Handles tool execution and detects delegation requests to spawn sub-agents.
"""

import json
import re
from typing import TYPE_CHECKING, Protocol, Callable, Optional

from src.utils.json import parse_tool_arguments
from src.tools.delegate import is_delegation_result, get_delegation_info

if TYPE_CHECKING:
    from src.tools.manager import ToolManager
    from src.subagents.runner import SubagentRunner


class UIProtocol(Protocol):
    def print_info(self, message: str) -> None: ...
    def show_preparing_tool(self, name: str, args: dict) -> None: ...
    def show_tool_execution(self, name: str, args: dict, success: bool, result: str) -> None: ...
    async def wait_for_user_approval(self, content: str) -> tuple: ...


class ToolExecutor:
    
    ERROR_PATTERNS = [
        (r'File "([^"]+)", line (\d+)', r'File "\1:\2"'),
        (r'^\s+at .+\n', ''),
        (r'\n\s*\n+', '\n'),
    ]
    
    def __init__(
        self, 
        tool_manager: "ToolManager", 
        ui_manager: UIProtocol = None,
        add_message_callback: Callable = None,
        max_error_length: int = 800,
        subagent_runner: Optional["SubagentRunner"] = None
    ):
        self._tool_manager = tool_manager
        self._ui_manager = ui_manager
        self._add_message = add_message_callback
        self._max_error_length = max_error_length
        self._subagent_runner = subagent_runner

    def set_subagent_runner(self, runner: "SubagentRunner") -> None:
        """Set the sub-agent runner for delegation."""
        self._subagent_runner = runner

    def _compact_error(self, error: str) -> str:
        if len(error) <= self._max_error_length:
            return error
        
        for pattern, replacement in self.ERROR_PATTERNS:
            error = re.sub(pattern, replacement, error, flags=re.MULTILINE)
        
        if len(error) <= self._max_error_length:
            return error.strip()
        
        lines = error.strip().split('\n')
        if len(lines) <= 6:
            return error[:self._max_error_length]
        
        head = '\n'.join(lines[:2])
        tail = '\n'.join(lines[-3:])
        omitted = len(lines) - 5
        return f"{head}\n[...{omitted} lines omitted...]\n{tail}"

    async def handle_tool_calls(self, tool_calls, get_reminders: Callable = None) -> None:
        for i, tool_call in enumerate(tool_calls):
            is_last_tool = (i == len(tool_calls) - 1)
            
            args, error = parse_tool_arguments(tool_call.function.arguments)
            if error:
                self._add_tool_response(tool_call, json.dumps({"error": error}), is_last_tool, get_reminders)
                continue

            need_user_approve = args.get('need_user_approve', False)
            should_execute = True
            user_content = ""

            if need_user_approve and self._ui_manager:
                approval_content = f"Tool: {tool_call.function.name}, args: {args}"
                should_execute, user_content = await self._ui_manager.wait_for_user_approval(approval_content)

            if should_execute:
                await self._execute_tool(tool_call, args, is_last_tool, get_reminders)
            else:
                self._add_tool_response(
                    tool_call, 
                    f"User denied execution. User input: {user_content}", 
                    is_last_tool,
                    get_reminders
                )

    async def _execute_tool(self, tool_call, args: dict, is_last_tool: bool, get_reminders: Callable) -> None:
        tool_args = {k: v for k, v in args.items() if k != 'need_user_approve'}
        
        if self._ui_manager:
            self._ui_manager.show_preparing_tool(tool_call.function.name, tool_args)
        
        tool_response = await self._safe_run_tool(tool_call.function.name, tool_args)
        
        # Check for delegation request
        if is_delegation_result(tool_response):
            tool_response = await self._handle_delegation(tool_response)
        
        success = "error" not in tool_response
        
        if self._ui_manager:
            self._ui_manager.show_tool_execution(
                tool_call.function.name, 
                tool_args, 
                success=success, 
                result=str(tool_response)[:200]  # Truncate for display
            )
        
        self._add_tool_response(tool_call, json.dumps(tool_response), is_last_tool, get_reminders)

    async def _handle_delegation(self, delegation_result: dict) -> dict:
        """Handle a delegation request by spawning the sub-agent."""
        agent, task, context = get_delegation_info(delegation_result)
        
        if not self._subagent_runner:
            return {"error": "Delegation not available - no sub-agent runner configured"}
        
        if self._ui_manager:
            self._ui_manager.print_info(f"\n[Delegating to {agent}]")
        
        try:
            # Run the sub-agent
            answer = await self._subagent_runner.run(
                agent_name=agent,
                task=task,
                context=context,
                ui=self._ui_manager
            )
            
            if self._ui_manager:
                self._ui_manager.print_info(f"[{agent}] Complete\n")
            
            return {
                "result": answer,
                "delegated_to": agent
            }
            
        except Exception as e:
            return {"error": f"Delegation failed: {e}"}

    async def _safe_run_tool(self, tool_name: str, tool_args: dict) -> dict:
        result = await self._tool_manager.run_tool(tool_name, **tool_args)
        
        # Delegation results pass through directly
        if is_delegation_result(result):
            return result
        
        if isinstance(result, str) and result.startswith("Error"):
            return {"error": self._compact_error(result)}
        if isinstance(result, dict) and "error" in result:
            result["error"] = self._compact_error(str(result["error"]))
            return result
        return result if isinstance(result, dict) else {"result": result}

    def _add_tool_response(
        self, 
        tool_call, 
        content: str, 
        is_last_tool: bool,
        get_reminders: Callable = None
    ) -> None:
        tool_content = [{"type": "text", "text": content}]
        
        if is_last_tool and get_reminders:
            reminder_content = get_reminders(self._tool_manager)
            if reminder_content:
                tool_content.append({"type": "text", "text": reminder_content})
        
        tool_message = {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_call.function.name,
            "content": tool_content
        }
        
        if self._add_message:
            self._add_message(tool_message)
