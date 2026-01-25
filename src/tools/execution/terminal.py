import asyncio
import os
import signal
from typing import Optional
from src.tools.base import BaseTool
from src.tools.execution.truncation import truncate_output


TOOL_DESCRIPTION = """Execute a shell command and return its output.

Use this for:
- Running build commands, tests, linters
- Git operations (status, diff, commit, push)
- Installing dependencies
- Running tests

IMPORTANT GUIDELINES:
1. Use `workdir` parameter instead of `cd && command` patterns
2. Set need_user_approve=true for destructive commands (rm, sudo, git push --force)
3. For long outputs, results are automatically truncated with a file path for full content

DO NOT use this for:
- Reading files (use read_file instead)
- Writing/editing files (use edit_file, search_replace instead)  
- Searching code (use ripgrep, glob instead)

When debugging:
1. Write a small test script to reproduce the issue
2. Run it to see the actual error
3. Fix based on real error output
4. Delete test script when done"""


SIGKILL_TIMEOUT_MS = 200


class CmdRunner(BaseTool):
    def __init__(self, default_timeout: int = 120):
        super().__init__()
        self._default_timeout = default_timeout
        self._cwd = os.getcwd()

    @staticmethod
    def get_tool_name():
        return "cmd_runner"

    async def _kill_process(self, process):
        """Kill process with SIGTERM, wait, then SIGKILL if needed."""
        if process.returncode is not None:
            return
        
        try:
            # Try SIGTERM first
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=SIGKILL_TIMEOUT_MS / 1000)
            except asyncio.TimeoutError:
                # Force kill if still running
                process.kill()
                await process.wait()
        except ProcessLookupError:
            pass  # Process already dead

    async def act(
        self, 
        command: str,
        workdir: Optional[str] = None,
        description: Optional[str] = None,
        timeout: Optional[int] = None,
        need_user_approve: bool = False
    ):
        """
        Execute a shell command.
        
        Args:
            command: The shell command to execute
            workdir: Working directory (use this instead of cd &&)
            description: Brief description of what this command does
            timeout: Timeout in seconds (default 120)
            need_user_approve: Set true for dangerous commands
        """
        working_dir = workdir or self._cwd
        cmd_timeout = timeout or self._default_timeout
        
        if not os.path.isdir(working_dir):
            return {"error": f"Working directory not found: {working_dir}"}
        
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_dir,
                env={**os.environ, "PAGER": "cat"},
                start_new_session=True  # For proper process group kill
            )
            
            timed_out = False
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=cmd_timeout
                )
            except asyncio.TimeoutError:
                timed_out = True
                await self._kill_process(process)
                return {
                    "error": f"Command timed out after {cmd_timeout}s",
                    "command": command,
                    "description": description
                }
            
            stdout_text = stdout.decode("utf-8", errors="replace")
            stderr_text = stderr.decode("utf-8", errors="replace")
            
            raw_output = self._format_output(stdout_text, stderr_text, process.returncode)
            
            # Apply truncation
            truncated = truncate_output(raw_output)
            
            return {
                "result": truncated.content,
                "exit_code": process.returncode,
                "success": process.returncode == 0,
                "truncated": truncated.truncated,
                "output_path": truncated.output_path,
                "description": description
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
                        "workdir": {
                            "type": "string",
                            "description": "Working directory for the command. Use this instead of 'cd && command' patterns."
                        },
                        "description": {
                            "type": "string",
                            "description": "Brief description of what this command does (5-10 words)."
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
