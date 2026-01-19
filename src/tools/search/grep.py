import asyncio
import os
from typing import Optional, List
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Search for text patterns in files using grep.

Useful for:
- Finding function definitions, class names, or variable usage
- Locating specific strings or patterns across the codebase
- Tracking down error messages or log entries

Returns matching lines with file paths and line numbers.
Supports basic regex patterns and case-insensitive search."""


class GrepSearchTool(BaseTool):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_tool_name():
        return "grep_search"

    async def act(
        self,
        pattern: str,
        path: str,
        include: Optional[str] = None,
        exclude: Optional[List[str]] = None,
        case_sensitive: bool = True,
        max_results: int = 100
    ):
        if not os.path.exists(path):
            return {"error": f"Path not found: {path}"}
        
        cmd_parts = ["grep", "-rn", "--color=never"]
        
        if not case_sensitive:
            cmd_parts.append("-i")
        
        if include:
            cmd_parts.extend(["--include", include])
        
        default_excludes = [".git", "node_modules", "__pycache__", ".venv", "venv", "*.pyc"]
        excludes = exclude if exclude else default_excludes
        for exc in excludes:
            cmd_parts.extend(["--exclude-dir" if not exc.startswith("*") else "--exclude", exc])
        
        cmd_parts.extend(["-e", pattern, path])
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd_parts,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=30
            )
            
            output = stdout.decode("utf-8", errors="replace")
            
            if not output.strip():
                return {"result": "No matches found", "matches": []}
            
            lines = output.strip().split("\n")
            matches = []
            
            for line in lines[:max_results]:
                try:
                    if ":" in line:
                        parts = line.split(":", 2)
                        if len(parts) >= 3:
                            matches.append({
                                "file": parts[0],
                                "line": int(parts[1]),
                                "content": parts[2].strip()
                            })
                except (ValueError, IndexError):
                    continue
            
            truncated = len(lines) > max_results
            
            return {
                "result": f"Found {len(matches)} matches",
                "matches": matches,
                "truncated": truncated
            }
            
        except asyncio.TimeoutError:
            return {"error": "Search timed out"}
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

    def json_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.get_tool_name(),
                "description": TOOL_DESCRIPTION,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "The text pattern to search for (supports basic regex)."
                        },
                        "path": {
                            "type": "string",
                            "description": "The directory or file path to search in."
                        },
                        "include": {
                            "type": "string",
                            "description": "File pattern to include (e.g., '*.py', '*.js')."
                        },
                        "case_sensitive": {
                            "type": "boolean",
                            "description": "Whether search is case-sensitive. Default true.",
                            "default": True
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results to return. Default 100.",
                            "default": 100
                        }
                    },
                    "required": ["pattern", "path"]
                }
            }
        }
