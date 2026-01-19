from typing import Optional, Protocol
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """A scratchpad for thinking through complex problems.

Use this as a workspace to:
- Break down complex tasks
- Outline approaches before implementation
- Keep track of thoughts during multi-step operations

The content is displayed to the user and can help show your reasoning process."""


class UIProtocol(Protocol):
    def print_info(self, message: str) -> None: ...


class ScratchpadTool(BaseTool):
    def __init__(self, ui_manager: Optional[UIProtocol] = None):
        super().__init__()
        self._ui_manager = ui_manager
        self._content = ""

    @staticmethod
    def get_tool_name():
        return "scratchpad"

    async def act(self, content: str, append: bool = False):
        if not content:
            return {"error": "Content is required"}
        
        if append:
            self._content += "\n" + content
        else:
            self._content = content
        
        if self._ui_manager:
            self._ui_manager.print_info(f"[Scratchpad]\n{self._content}")
        
        return {
            "result": "Scratchpad updated",
            "content": self._content
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
                        "content": {
                            "type": "string",
                            "description": "The content to write to the scratchpad."
                        },
                        "append": {
                            "type": "boolean",
                            "description": "Append to existing content instead of replacing. Default false.",
                            "default": False
                        }
                    },
                    "required": ["content"]
                }
            }
        }
