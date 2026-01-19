from pathlib import Path
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Edit a file by replacing its entire content or creating a new file.

Use this for:
- Creating new files with specified content
- Completely rewriting existing files
- Making significant changes where search/replace would be cumbersome

The file will be created if it doesn't exist, including any necessary parent directories.
Returns confirmation of the edit or an error message."""


class EditFileTool(BaseTool):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_tool_name():
        return "edit_file"

    async def act(self, file_path: str, content: str, create_dirs: bool = True):
        path = Path(file_path)
        
        try:
            if create_dirs:
                path.parent.mkdir(parents=True, exist_ok=True)
            
            is_new = not path.exists()
            
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            
            action = "Created" if is_new else "Updated"
            line_count = content.count('\n') + (1 if content and not content.endswith('\n') else 0)
            
            return {
                "result": f"{action} {file_path}",
                "lines": line_count,
                "bytes": len(content.encode('utf-8'))
            }
            
        except PermissionError:
            return {"error": f"Permission denied: {file_path}"}
        except Exception as e:
            return {"error": f"Failed to edit file: {str(e)}"}

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
                            "description": "The absolute path to the file to edit or create."
                        },
                        "content": {
                            "type": "string",
                            "description": "The new content to write to the file."
                        },
                        "create_dirs": {
                            "type": "boolean",
                            "description": "Whether to create parent directories if they don't exist. Default true.",
                            "default": True
                        }
                    },
                    "required": ["file_path", "content"]
                }
            }
        }
