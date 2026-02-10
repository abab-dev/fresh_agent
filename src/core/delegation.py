"""Delegation tool - returns Handoff intent for Runner to handle."""

from .models import Handoff


class DelegateTool:
    name = "delegate"
    available_agents: list[str] = []
    
    def schema(self) -> dict:
        agents_enum = self.available_agents if self.available_agents else ["explorer"]
        
        return {
            "type": "function",
            "function": {
                "name": "delegate",
                "description": "Delegate a task to a specialized sub-agent.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent": {
                            "type": "string",
                            "enum": agents_enum,
                            "description": "The sub-agent type to delegate to.",
                        },
                        "task": {
                            "type": "string",
                            "description": "The task for the sub-agent. Be detailed.",
                        },
                    },
                    "required": ["agent", "task"],
                },
            },
        }
    
    async def execute(self, agent: str, task: str) -> Handoff:
        return Handoff(agent=agent, task=task)
