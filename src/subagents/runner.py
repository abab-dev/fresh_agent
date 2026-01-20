"""
SubagentRunner - executes sub-agents with restricted tools.

Takes a task and sub-agent config, runs a mini agent loop,
and returns the final answer.
"""

import json
import logging
from typing import Any, Dict, List, Optional

from src.subagents.manager import SubagentManager, SubagentConfig

logger = logging.getLogger(__name__)


class SubagentRunner:
    """
    Runs a sub-agent with restricted tools.
    
    This creates a mini agent loop that:
    1. Uses the sub-agent's system prompt
    2. Only allows the sub-agent's specified tools
    3. Runs until the sub-agent completes
    4. Returns the final answer
    """
    
    def __init__(
        self,
        llm_client,
        tool_manager,
        subagent_manager: SubagentManager,
        max_iterations: int = 10
    ):
        self.llm_client = llm_client
        self.tool_manager = tool_manager
        self.subagent_manager = subagent_manager
        self.max_iterations = max_iterations
    
    def _get_restricted_tools(self, allowed_tool_names: List[str]) -> List[Dict]:
        """Get tool schemas for only the allowed tools."""
        all_tools = self.tool_manager.get_tools_description()
        return [t for t in all_tools if t["function"]["name"] in allowed_tool_names]
    
    async def run(
        self,
        agent_name: str,
        task: str,
        context: Optional[str] = None,
        ui=None
    ) -> str:
        """
        Run a sub-agent and return its final answer.
        
        Args:
            agent_name: Name of the sub-agent (e.g., "explorer")
            task: The task/question for the sub-agent
            context: Optional additional context
            ui: Optional UI for displaying progress
            
        Returns:
            The sub-agent's final answer as a string
        """
        # Lazy import to avoid circular dependency
        from src.agent.message import MessageBuilder
        
        # Get sub-agent config
        try:
            config = self.subagent_manager.get_subagent(agent_name)
        except ValueError as e:
            return f"Error: {e}"
        
        # Emit subagent handoff event
        if ui:
            if hasattr(ui, 'subagent_start'):
                ui.subagent_start(agent_name, task)
            else:
                ui.print_info(f"[{agent_name}] Starting...")
        
        # Build the task message
        task_content = task
        if context:
            task_content = f"{task}\n\nContext:\n{context}"
        
        # Get restricted tools
        allowed_tools = self._get_restricted_tools(config.tools)
        
        if not allowed_tools:
            return f"Error: No valid tools available for sub-agent '{agent_name}'"
        
        # Build messages
        messages = [
            MessageBuilder.create_system_message(config.prompt),
            MessageBuilder.create_user_message(task_content)
        ]
        
        # Mini agent loop
        for iteration in range(self.max_iterations):
            try:
                # Get LLM response - returns (message, token_usage) tuple
                # LLMClient.get_completion expects request_params dict
                message, _ = self.llm_client.get_completion({
                    "messages": messages,
                    "tools": allowed_tools
                })
                
                # Convert ChatCompletionMessage to dict for storage
                assistant_msg = {
                    "role": "assistant",
                    "content": message.content
                }
                
                # Handle tool calls - response is ChatCompletionMessage object
                tool_calls = message.tool_calls or []
                
                if tool_calls:
                    # Serialize tool calls for message history
                    assistant_msg["tool_calls"] = [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in tool_calls
                    ]
                
                messages.append(assistant_msg)
                
                # Check if done (no tool calls)
                if not tool_calls:
                    # Sub-agent is done
                    final_answer = message.content or ""
                    if ui:
                        if hasattr(ui, 'subagent_complete'):
                            ui.subagent_complete(agent_name, final_answer)
                        else:
                            ui.print_info(f"[{agent_name}] Done")
                    return final_answer
                
                # Execute tool calls - tool_calls are ChatCompletionMessageToolCall objects
                for tool_call in tool_calls:
                    tool_name = tool_call.function.name
                    tool_args_raw = tool_call.function.arguments
                    tool_id = tool_call.id
                    
                    # Parse arguments - always a JSON string from OpenAI
                    if isinstance(tool_args_raw, str):
                        try:
                            tool_args = json.loads(tool_args_raw)
                        except json.JSONDecodeError:
                            tool_args = {}
                    else:
                        tool_args = tool_args_raw if isinstance(tool_args_raw, dict) else {}
                    
                    # Emit subagent tool event
                    if ui and hasattr(ui, 'subagent_tool'):
                        ui.subagent_tool(agent_name, tool_name, tool_args)
                    
                    # Verify tool is allowed
                    if tool_name not in config.tools:
                        result = f"Error: Tool '{tool_name}' not allowed for this sub-agent"
                        success = False
                    else:
                        try:
                            result = await self.tool_manager.run_tool(tool_name, **tool_args)
                            success = True
                        except Exception as e:
                            result = f"Error: {e}"
                            success = False
                    
                    # Emit subagent tool result event
                    if ui:
                        if hasattr(ui, 'subagent_tool_result'):
                            ui.subagent_tool_result(agent_name, tool_name, success, str(result))
                        else:
                            ui.print_info(f"  [{agent_name}] {tool_name}(...)")
                    
                    # Add tool result
                    messages.append(
                        MessageBuilder.create_tool_message(
                            tool_call_id=tool_id,
                            name=tool_name,
                            content=str(result)
                        )
                    )
                
            except Exception as e:
                logger.error(f"Sub-agent error: {e}")
                return f"Sub-agent error: {e}"
        
        # Max iterations reached
        return "Sub-agent reached maximum iterations without completing."
    
    async def run_explorer(self, task: str, context: Optional[str] = None, ui=None) -> str:
        """Convenience method to run the explorer sub-agent."""
        return await self.run("explorer", task, context, ui)
