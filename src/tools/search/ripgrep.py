"""
Ripgrep-based text search with automatic fallback to grep.

Provides fast, intelligent code search with:
- Automatic .gitignore respect
- Context lines before/after matches
- File type filtering
- Regex support
"""

import asyncio
import os
import shutil
from typing import Optional, List
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Search for text patterns in files using ripgrep (with grep fallback).

This is the PRIMARY tool for searching code. Uses ripgrep when available (10x faster),
automatically falls back to grep.

Features:
- Respects .gitignore by default
- Returns file, line number, and matching content
- Supports regex patterns
- Can show context lines before/after matches
- Filter by file type (e.g., 'py', 'js', 'ts')

Use cases:
- Find function/class definitions
- Locate string literals or error messages
- Track down variable usage
- Search for TODO/FIXME comments"""


class RipgrepTool(BaseTool):
    def __init__(self):
        super().__init__()
        self._has_ripgrep = shutil.which("rg") is not None

    @staticmethod
    def get_tool_name():
        return "ripgrep"

    async def act(
        self,
        pattern: str,
        path: str,
        file_type: Optional[str] = None,
        include_pattern: Optional[str] = None,
        case_sensitive: bool = True,
        context_before: int = 0,
        context_after: int = 0,
        max_results: int = 100,
        regex: bool = False
    ):
        """
        Search for pattern in files.
        
        Args:
            pattern: Text or regex pattern to search for
            path: Directory or file to search in
            file_type: Filter by file type (e.g., 'py', 'js', 'ts', 'go')
            include_pattern: Glob pattern for files to include (e.g., '*.py')
            case_sensitive: Case-sensitive search (default True)
            context_before: Lines of context before match
            context_after: Lines of context after match
            max_results: Maximum number of matches to return
            regex: Treat pattern as regex (default False = literal search)
        """
        if not os.path.exists(path):
            return {"error": f"Path not found: {path}"}
        
        if self._has_ripgrep:
            return await self._search_ripgrep(
                pattern, path, file_type, include_pattern,
                case_sensitive, context_before, context_after,
                max_results, regex
            )
        else:
            return await self._search_grep(
                pattern, path, include_pattern,
                case_sensitive, max_results
            )

    async def _search_ripgrep(
        self, pattern, path, file_type, include_pattern,
        case_sensitive, context_before, context_after, max_results, regex
    ):
        cmd = ["rg", "--json", "--no-heading"]
        
        if not case_sensitive:
            cmd.append("-i")
        
        if not regex:
            cmd.append("-F")  # Fixed string (literal) search
        
        if file_type:
            cmd.extend(["-t", file_type])
        
        if include_pattern:
            cmd.extend(["-g", include_pattern])
        
        if context_before > 0:
            cmd.extend(["-B", str(context_before)])
        
        if context_after > 0:
            cmd.extend(["-A", str(context_after)])
        
        cmd.extend(["-m", str(max_results)])  # Max matches per file
        cmd.extend(["--", pattern, path])
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=60
            )
            
            output = stdout.decode("utf-8", errors="replace")
            matches = self._parse_ripgrep_json(output, max_results)
            
            return {
                "result": f"Found {len(matches)} matches",
                "matches": matches,
                "truncated": len(matches) >= max_results,
                "engine": "ripgrep"
            }
            
        except asyncio.TimeoutError:
            return {"error": "Search timed out after 60s"}
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

    def _parse_ripgrep_json(self, output: str, max_results: int) -> List[dict]:
        import json
        matches = []
        
        for line in output.strip().split("\n"):
            if not line:
                continue
            try:
                msg = json.loads(line)
                if msg.get("type") == "match":
                    data = msg.get("data", {})
                    file_path = data.get("path", {}).get("text", "")
                    line_num = data.get("line_number", 0)
                    
                    # Get match text
                    lines_data = data.get("lines", {})
                    content = lines_data.get("text", "").strip()
                    
                    matches.append({
                        "file": file_path,
                        "line": line_num,
                        "content": content[:500]  # Truncate long lines
                    })
                    
                    if len(matches) >= max_results:
                        break
            except json.JSONDecodeError:
                continue
        
        return matches

    async def _search_grep(
        self, pattern, path, include_pattern, case_sensitive, max_results
    ):
        cmd = ["grep", "-rn", "--color=never", "-F"]  # -F for literal
        
        if not case_sensitive:
            cmd.append("-i")
        
        if include_pattern:
            cmd.extend(["--include", include_pattern])
        
        # Default excludes
        for exc in [".git", "node_modules", "__pycache__", ".venv", "venv"]:
            cmd.extend(["--exclude-dir", exc])
        
        cmd.extend(["--", pattern, path])
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, _ = await asyncio.wait_for(
                process.communicate(),
                timeout=60
            )
            
            output = stdout.decode("utf-8", errors="replace")
            matches = []
            
            for line in output.strip().split("\n")[:max_results]:
                if ":" in line:
                    parts = line.split(":", 2)
                    if len(parts) >= 3:
                        matches.append({
                            "file": parts[0],
                            "line": int(parts[1]) if parts[1].isdigit() else 0,
                            "content": parts[2].strip()[:500]
                        })
            
            return {
                "result": f"Found {len(matches)} matches",
                "matches": matches,
                "truncated": len(matches) >= max_results,
                "engine": "grep"
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
                            "description": "The text pattern to search for."
                        },
                        "path": {
                            "type": "string",
                            "description": "Directory or file to search in (absolute path)."
                        },
                        "file_type": {
                            "type": "string",
                            "description": "Filter by file type: 'py', 'js', 'ts', 'go', 'rs', 'java', etc."
                        },
                        "include_pattern": {
                            "type": "string",
                            "description": "Glob pattern for files to include (e.g., '*.py', 'test_*.js')."
                        },
                        "case_sensitive": {
                            "type": "boolean",
                            "description": "Case-sensitive search. Default true.",
                            "default": True
                        },
                        "context_before": {
                            "type": "integer",
                            "description": "Lines of context before each match. Default 0.",
                            "default": 0
                        },
                        "context_after": {
                            "type": "integer", 
                            "description": "Lines of context after each match. Default 0.",
                            "default": 0
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum matches to return. Default 100.",
                            "default": 100
                        },
                        "regex": {
                            "type": "boolean",
                            "description": "Treat pattern as regex. Default false (literal search).",
                            "default": False
                        }
                    },
                    "required": ["pattern", "path"]
                }
            }
        }
