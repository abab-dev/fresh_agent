import os
from typing import Optional
from src.tools.base import BaseTool
from src.code_analysis.context_provider import ContextProvider


TOOL_DESCRIPTION = """Get semantic context around a specific line in a source file.

Given a file path and line number, this tool finds the containing function, class,
or method and returns its full code. This is much more useful than just returning
a fixed number of lines around the target.

Use cases:
- After grep finds a match, expand to see the full function
- Understand what function a specific line belongs to
- Get complete context when debugging or reviewing code

Falls back to a fixed-size code chunk if no containing symbol is found."""


class GetContextTool(BaseTool):
    def __init__(self):
        super().__init__()
        self._provider = ContextProvider()

    @staticmethod
    def get_tool_name():
        return "get_context"

    async def act(
        self,
        file_path: str,
        line: int,
        context_lines: int = 15
    ):
        """
        Get the semantic context around a line.
        
        Args:
            file_path: Absolute path to the source file
            line: Line number (1-indexed)
            context_lines: Fallback context size if no containing symbol found
        """
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}
        
        if not os.path.isfile(file_path):
            return {"error": f"Not a file: {file_path}"}
        
        if line < 1:
            return {"error": "Line number must be >= 1"}
        
        context = self._provider.get_context_around_line(
            file_path, 
            line, 
            context_lines=context_lines
        )
        
        if context is None:
            return {"error": f"Could not extract context for line {line}"}
        
        return context.to_dict()

    def json_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.get_tool_name(),
                "description": TOOL_DESCRIPTION,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Absolute path to the source file."
                        },
                        "line": {
                            "type": "integer",
                            "description": "Line number to get context for (1-indexed)."
                        },
                        "context_lines": {
                            "type": "integer",
                            "description": "Fallback: lines of context if no containing symbol. Default 15.",
                            "default": 15
                        }
                    },
                    "required": ["file_path", "line"]
                }
            }
        }
