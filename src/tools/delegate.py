"""
Generic delegate tool for spawning sub-agents.

The main agent calls this to delegate tasks to specialized sub-agents.
The executor detects the delegation marker and spawns the appropriate sub-agent.
"""

from typing import Optional, List
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Delegate a task to a specialized sub-agent.

Available sub-agents:
- **explorer**: Codebase search specialist. Use for "where is X?", "how does X work?", 
  finding files, understanding architecture. Returns direct answers with file evidence.

USE THIS WHEN:
- User asks "Where is X?" or "How does X work?"
- You need to search across many files
- You need to understand code relationships
- User is confused about implementation details

DO NOT USE WHEN:
- You already know the exact file path
- Making a simple edit to a known file
- Running a command

The sub-agent runs with restricted tools and returns a structured answer."""


class DelegateTool(BaseTool):
    """
    Generic delegation tool.
    
    Returns a marker that the executor detects to spawn the sub-agent.
    """
    
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def get_tool_name():
        return "delegate"
    
    async def act(
        self,
        agent: str,
        task: str,
        context: Optional[str] = None
    ):
        """
        Delegate a task to a sub-agent.
        
        Args:
            agent: Sub-agent to use (e.g., "explorer")
            task: The task/question for the sub-agent. Be specific.
            context: Optional additional context to help the sub-agent.
        """
        # Return a marker that the executor will detect
        return {
            "_delegate": True,
            "agent": agent,
            "task": task,
            "context": context
        }
    
    def json_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.get_tool_name(),
                "description": TOOL_DESCRIPTION,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent": {
                            "type": "string",
                            "enum": ["explorer"],  # Add more as we create them
                            "description": "The sub-agent to delegate to."
                        },
                        "task": {
                            "type": "string",
                            "description": """The task or question for the sub-agent. Be specific:

For explorer, use this format:
QUESTION: [What you need to find out]
KEYWORDS: [Search terms to look for]
EXPECTED: [What kind of answer you need]"""
                        },
                        "context": {
                            "type": "string",
                            "description": "Optional context to help the sub-agent."
                        }
                    },
                    "required": ["agent", "task"]
                }
            }
        }


def is_delegation_result(result: dict) -> bool:
    """Check if a tool result is a delegation request."""
    return isinstance(result, dict) and result.get("_delegate") is True


def get_delegation_info(result: dict) -> tuple:
    """Extract delegation info from result. Returns (agent, task, context)."""
    return (
        result.get("agent"),
        result.get("task"),
        result.get("context")
    )
