import asyncio
import os
from typing import Optional, List
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Commit changes to the git repository.

This will:
1. Stage specified files (or all changes if no files specified)
2. Create a commit with the provided message

IMPORTANT: Set need_user_approve=true when making commits.
Always write meaningful commit messages that describe the changes."""


class GitCommitTool(BaseTool):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_tool_name():
        return "git_commit"

    async def act(
        self,
        message: str,
        path: Optional[str] = None,
        files: Optional[List[str]] = None,
        all_changes: bool = True,
        need_user_approve: bool = True
    ):
        cwd = path or os.getcwd()
        
        if not os.path.isdir(cwd):
            return {"error": f"Directory not found: {cwd}"}
        
        if not message or not message.strip():
            return {"error": "Commit message is required"}
        
        try:
            if files:
                add_cmd = ["git", "add"] + files
            elif all_changes:
                add_cmd = ["git", "add", "-A"]
            else:
                add_cmd = None
            
            if add_cmd:
                process = await asyncio.create_subprocess_exec(
                    *add_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=cwd
                )
                _, stderr = await asyncio.wait_for(process.communicate(), timeout=10)
                
                if process.returncode != 0:
                    return {"error": f"Git add failed: {stderr.decode()}"}
            
            process = await asyncio.create_subprocess_exec(
                "git", "commit", "-m", message,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=10
            )
            
            if process.returncode != 0:
                error_msg = stderr.decode("utf-8", errors="replace").strip()
                if "nothing to commit" in error_msg.lower() or "nothing to commit" in stdout.decode().lower():
                    return {"result": "Nothing to commit", "committed": False}
                return {"error": error_msg}
            
            output = stdout.decode("utf-8", errors="replace").strip()
            
            return {
                "result": "Commit successful",
                "committed": True,
                "output": output
            }
            
        except asyncio.TimeoutError:
            return {"error": "Git commit timed out"}
        except FileNotFoundError:
            return {"error": "Git is not installed"}
        except Exception as e:
            return {"error": f"Git commit failed: {str(e)}"}

    def json_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.get_tool_name(),
                "description": TOOL_DESCRIPTION,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The commit message describing the changes."
                        },
                        "path": {
                            "type": "string",
                            "description": "Path to git repository. Defaults to current directory."
                        },
                        "files": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Specific files to stage and commit."
                        },
                        "all_changes": {
                            "type": "boolean",
                            "description": "Stage all changes before commit. Default true.",
                            "default": True
                        },
                        "need_user_approve": {
                            "type": "boolean",
                            "description": "Request user approval. Default true (recommended).",
                            "default": True
                        }
                    },
                    "required": ["message"]
                }
            }
        }
