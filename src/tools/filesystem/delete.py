import os
import shutil
from pathlib import Path
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Delete a file or directory from the filesystem.

CAUTION: This is a destructive operation that cannot be undone.
Always set need_user_approve=true when deleting files.

For directories, use recursive=true to delete non-empty directories.
The tool will refuse to delete certain protected paths."""


PROTECTED_PATHS = {
    "/", "/home", "/usr", "/bin", "/sbin", "/etc", "/var", "/tmp",
    "/root", "/boot", "/dev", "/proc", "/sys"
}


class DeleteFileTool(BaseTool):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_tool_name():
        return "delete_file"

    async def act(
        self, 
        path: str, 
        recursive: bool = False,
        need_user_approve: bool = True
    ):
        target = Path(path).resolve()
        
        if str(target) in PROTECTED_PATHS:
            return {"error": f"Cannot delete protected path: {path}"}
        
        if not target.exists():
            return {"error": f"Path not found: {path}"}
        
        try:
            if target.is_file():
                size = target.stat().st_size
                target.unlink()
                return {"result": f"Deleted file: {path}", "bytes_freed": size}
            
            elif target.is_dir():
                if not recursive and any(target.iterdir()):
                    return {"error": f"Directory not empty. Use recursive=true to delete: {path}"}
                
                if recursive:
                    shutil.rmtree(target)
                else:
                    target.rmdir()
                    
                return {"result": f"Deleted directory: {path}"}
            
            else:
                return {"error": f"Unknown file type: {path}"}
                
        except PermissionError:
            return {"error": f"Permission denied: {path}"}
        except Exception as e:
            return {"error": f"Failed to delete: {str(e)}"}

    def json_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.get_tool_name(),
                "description": TOOL_DESCRIPTION,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The absolute path to the file or directory to delete."
                        },
                        "recursive": {
                            "type": "boolean",
                            "description": "For directories: delete contents recursively. Default false.",
                            "default": False
                        },
                        "need_user_approve": {
                            "type": "boolean",
                            "description": "Request user approval before deletion. Default true (recommended).",
                            "default": True
                        }
                    },
                    "required": ["path"]
                }
            }
        }
