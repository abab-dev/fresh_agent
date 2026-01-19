"""
SubagentRunner - executes sub-agents with restricted tools.

Takes a task and sub-agent config, runs a mini agent loop,
and returns the final answer.
"""

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
        all_tools = self.tool_manager.get_tool_descriptions()
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
        
        if ui:
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
            MessageBuilder.create_system(config.prompt),
            MessageBuilder.create_user(task_content)
        ]
        
        # Mini agent loop
        for iteration in range(self.max_iterations):
            try:
                # Get LLM response
                response = await self.llm_client.get_completion(
                    messages=messages,
                    tools=allowed_tools
                )
                
                # Add assistant message
                messages.append(response)
                
                # Check if done (no tool calls)
                tool_calls = response.get("tool_calls", [])
                if not tool_calls:
                    # Sub-agent is done
                    final_answer = response.get("content", "")
                    if ui:
                        ui.print_info(f"[{agent_name}] Done")
                    return final_answer
                
                # Execute tool calls
                for tool_call in tool_calls:
                    tool_name = tool_call.get("function", {}).get("name")
                    tool_args = tool_call.get("function", {}).get("arguments", {})
                    tool_id = tool_call.get("id")
                    
                    # Verify tool is allowed
                    if tool_name not in config.tools:
                        result = f"Error: Tool '{tool_name}' not allowed for this sub-agent"
                    else:
                        try:
                            result = await self.tool_manager.run_tool(tool_name, tool_args)
                            if ui:
                                ui.print_info(f"  [{agent_name}] {tool_name}(...)")
                        except Exception as e:
                            result = f"Error: {e}"
                    
                    # Add tool result
                    messages.append(
                        MessageBuilder.create_tool_result(
                            tool_call_id=tool_id,
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
