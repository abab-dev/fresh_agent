import asyncio
import os
from typing import Optional
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Show git diff for changes in the repository.

Options:
- staged: Show only staged changes (default: all changes)
- file_path: Show diff for a specific file only
- max_lines: Limit output length

Use this to review changes before committing or understand what was modified."""


class GitDiffTool(BaseTool):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_tool_name():
        return "git_diff"

    async def act(
        self,
        path: Optional[str] = None,
        staged: bool = False,
        file_path: Optional[str] = None,
        max_lines: int = 500
    ):
        cwd = path or os.getcwd()
        
        if not os.path.isdir(cwd):
            return {"error": f"Directory not found: {cwd}"}
        
        cmd = ["git", "diff", "--no-color"]
        if staged:
            cmd.append("--cached")
        if file_path:
            cmd.extend(["--", file_path])
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=30
            )
            
            if process.returncode != 0:
                error_msg = stderr.decode("utf-8", errors="replace").strip()
                return {"error": error_msg}
            
            output = stdout.decode("utf-8", errors="replace")
            
            if not output.strip():
                return {"result": "No changes", "diff": ""}
            
            lines = output.split("\n")
            truncated = len(lines) > max_lines
            
            if truncated:
                output = "\n".join(lines[:max_lines])
                output += f"\n\n[... truncated {len(lines) - max_lines} lines]"
            
            return {
                "result": f"Diff output ({len(lines)} lines)",
                "diff": output,
                "truncated": truncated
            }
            
        except asyncio.TimeoutError:
            return {"error": "Git diff timed out"}
        except FileNotFoundError:
            return {"error": "Git is not installed"}
        except Exception as e:
            return {"error": f"Git diff failed: {str(e)}"}

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
                        },
                        "staged": {
                            "type": "boolean",
                            "description": "Show only staged changes. Default false.",
                            "default": False
                        },
                        "file_path": {
                            "type": "string",
                            "description": "Show diff for a specific file only."
                        },
                        "max_lines": {
                            "type": "integer",
                            "description": "Maximum lines of diff output. Default 500.",
                            "default": 500
                        }
                    },
                    "required": []
                }
            }
        }
