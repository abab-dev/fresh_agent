import asyncio
import os
import subprocess
from typing import Optional
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Execute a shell command and return its output.

Use this for:
- Running build commands, tests, linters
- Checking system state (git status, file checks)
- Installing dependencies
- Any shell-based automation

IMPORTANT: Set need_user_approve=true for any potentially destructive command:
- Commands with sudo, rm, chmod, chown
- Package installations (pip install, npm install -g)
- Git push, git reset --hard
- Any command that modifies system state

The command runs in a bash shell with a configurable timeout."""


class CmdRunner(BaseTool):
    def __init__(self, default_timeout: int = 120):
        super().__init__()
        self._default_timeout = default_timeout
        self._cwd = os.getcwd()

    @staticmethod
    def get_tool_name():
        return "cmd_runner"

    async def act(
        self, 
        command: str,
        cwd: Optional[str] = None,
        timeout: Optional[int] = None,
        need_user_approve: bool = False
    ):
        working_dir = cwd or self._cwd
        cmd_timeout = timeout or self._default_timeout
        
        if not os.path.isdir(working_dir):
            return {"error": f"Working directory not found: {working_dir}"}
        
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_dir,
                env={**os.environ, "PAGER": "cat"}
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=cmd_timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return {
                    "error": f"Command timed out after {cmd_timeout}s",
                    "command": command
                }
            
            stdout_text = stdout.decode("utf-8", errors="replace")
            stderr_text = stderr.decode("utf-8", errors="replace")
            
            output = self._format_output(stdout_text, stderr_text, process.returncode)
            
            return {
                "result": output,
                "exit_code": process.returncode,
                "success": process.returncode == 0
            }
            
        except Exception as e:
            return {"error": f"Failed to execute command: {str(e)}"}

    def _format_output(self, stdout: str, stderr: str, exit_code: int) -> str:
        parts = []
        
        if stdout.strip():
            parts.append(stdout.strip())
        
        if stderr.strip():
            parts.append(f"[stderr]\n{stderr.strip()}")
        
        if exit_code != 0:
            parts.append(f"[exit code: {exit_code}]")
        
        return "\n".join(parts) if parts else "(no output)"

    def json_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.get_tool_name(),
                "description": TOOL_DESCRIPTION,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The shell command to execute."
                        },
                        "cwd": {
                            "type": "string",
                            "description": "Working directory for the command. Defaults to current directory."
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Timeout in seconds. Default 120.",
                            "default": 120
                        },
                        "need_user_approve": {
                            "type": "boolean",
                            "description": "Set to true for potentially dangerous commands.",
                            "default": False
                        }
                    },
                    "required": ["command"]
                }
            }
        }
