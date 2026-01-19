import asyncio
import os
from typing import Optional
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Get the current git status of a repository.

Shows:
- Modified, added, deleted, and untracked files
- Current branch
- Ahead/behind status relative to remote

Use this to understand the current state of changes before committing."""


class GitStatusTool(BaseTool):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_tool_name():
        return "git_status"

    async def act(self, path: Optional[str] = None):
        cwd = path or os.getcwd()
        
        if not os.path.isdir(cwd):
            return {"error": f"Directory not found: {cwd}"}
        
        try:
            process = await asyncio.create_subprocess_exec(
                "git", "status", "--porcelain=v2", "--branch",
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
                if "not a git repository" in error_msg.lower():
                    return {"error": "Not a git repository"}
                return {"error": error_msg}
            
            output = stdout.decode("utf-8", errors="replace")
            result = self._parse_status(output)
            result["path"] = cwd
            
            return result
            
        except asyncio.TimeoutError:
            return {"error": "Git status timed out"}
        except FileNotFoundError:
            return {"error": "Git is not installed"}
        except Exception as e:
            return {"error": f"Git status failed: {str(e)}"}

    def _parse_status(self, output: str) -> dict:
        result = {
            "branch": None,
            "modified": [],
            "added": [],
            "deleted": [],
            "untracked": [],
            "renamed": []
        }
        
        for line in output.strip().split("\n"):
            if not line:
                continue
            
            if line.startswith("# branch.head"):
                result["branch"] = line.split()[-1]
            elif line.startswith("1 ") or line.startswith("2 "):
                parts = line.split()
                if len(parts) >= 9:
                    xy = parts[1]
                    filename = parts[-1]
                    
                    if xy[0] == "M" or xy[1] == "M":
                        result["modified"].append(filename)
                    elif xy[0] == "A":
                        result["added"].append(filename)
                    elif xy[0] == "D" or xy[1] == "D":
                        result["deleted"].append(filename)
                    elif xy[0] == "R":
                        result["renamed"].append(filename)
            elif line.startswith("? "):
                result["untracked"].append(line[2:])
        
        return result

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
                            "description": "Path to git repository. Defaults to current directory."
                        }
                    },
                    "required": []
                }
            }
        }
