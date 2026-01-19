"""
Glob-based file finder using fd or find.

Fast file discovery with pattern matching and type filtering.
"""

import asyncio
import os
import shutil
from pathlib import Path
from typing import Optional, List
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Find files and directories using glob patterns.

Uses fd (fast find) when available, falls back to find command.

Features:
- Glob pattern matching (e.g., '*.py', 'test_*.js', '**/config.*')
- Filter by type (file, directory, or both)
- Respects .gitignore by default
- Limit search depth
- Filter by extension

Use cases:
- Find all Python files in a project
- Locate configuration files
- Discover test files
- Find files by partial name"""


class GlobTool(BaseTool):
    def __init__(self):
        super().__init__()
        self._has_fd = shutil.which("fd") is not None

    @staticmethod
    def get_tool_name():
        return "glob"

    async def act(
        self,
        pattern: str,
        path: str,
        file_type: Optional[str] = None,
        extensions: Optional[List[str]] = None,
        max_depth: Optional[int] = None,
        include_hidden: bool = False,
        max_results: int = 100
    ):
        """
        Find files matching a pattern.
        
        Args:
            pattern: Glob pattern (e.g., '*.py', 'test_*', '**/config.*')
            path: Directory to search in
            file_type: 'file', 'directory', or None for both
            extensions: List of extensions to include (e.g., ['py', 'js'])
            max_depth: Maximum directory depth to search
            include_hidden: Include hidden files/directories
            max_results: Maximum results to return
        """
        if not os.path.exists(path):
            return {"error": f"Path not found: {path}"}
        
        if not os.path.isdir(path):
            return {"error": f"Not a directory: {path}"}
        
        if self._has_fd:
            return await self._search_fd(
                pattern, path, file_type, extensions,
                max_depth, include_hidden, max_results
            )
        else:
            return await self._search_find(
                pattern, path, file_type,
                max_depth, include_hidden, max_results
            )

    async def _search_fd(
        self, pattern, path, file_type, extensions,
        max_depth, include_hidden, max_results
    ):
        cmd = ["fd", "--glob"]  # Use glob pattern syntax
        
        if file_type == "file":
            cmd.extend(["--type", "f"])
        elif file_type == "directory":
            cmd.extend(["--type", "d"])
        
        if extensions:
            for ext in extensions:
                cmd.extend(["-e", ext.lstrip(".")])
        
        if max_depth:
            cmd.extend(["--max-depth", str(max_depth)])
        
        if include_hidden:
            cmd.append("--hidden")
        
        cmd.extend(["--max-results", str(max_results)])
        cmd.extend(["--", pattern, path])
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, _ = await asyncio.wait_for(
                process.communicate(),
                timeout=30
            )
            
            output = stdout.decode("utf-8", errors="replace")
            files = self._parse_results(output, path, max_results)
            
            return {
                "result": f"Found {len(files)} items",
                "files": files,
                "truncated": len(files) >= max_results,
                "engine": "fd"
            }
            
        except asyncio.TimeoutError:
            return {"error": "Search timed out"}
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

    async def _search_find(
        self, pattern, path, file_type,
        max_depth, include_hidden, max_results
    ):
        cmd = ["find", path]
        
        if max_depth:
            cmd.extend(["-maxdepth", str(max_depth)])
        
        if file_type == "file":
            cmd.extend(["-type", "f"])
        elif file_type == "directory":
            cmd.extend(["-type", "d"])
        
        # Exclude common directories
        for exc in [".git", "node_modules", "__pycache__", ".venv"]:
            cmd.extend(["-not", "-path", f"*/{exc}/*"])
        
        if not include_hidden:
            cmd.extend(["-not", "-name", ".*"])
        
        cmd.extend(["-name", pattern])
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, _ = await asyncio.wait_for(
                process.communicate(),
                timeout=30
            )
            
            output = stdout.decode("utf-8", errors="replace")
            files = self._parse_results(output, path, max_results)
            
            return {
                "result": f"Found {len(files)} items",
                "files": files,
                "truncated": len(files) >= max_results,
                "engine": "find"
            }
            
        except asyncio.TimeoutError:
            return {"error": "Search timed out"}
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

    def _parse_results(self, output: str, base_path: str, max_results: int) -> List[dict]:
        files = []
        base = Path(base_path).resolve()
        
        for line in output.strip().split("\n")[:max_results]:
            if not line:
                continue
            
            try:
                full_path = Path(line.strip()).resolve()
                
                try:
                    rel_path = full_path.relative_to(base)
                except ValueError:
                    rel_path = full_path
                
                info = {
                    "path": str(full_path),
                    "relative": str(rel_path),
                    "name": full_path.name,
                    "is_file": full_path.is_file()
                }
                
                if full_path.is_file():
                    try:
                        info["size"] = full_path.stat().st_size
                    except OSError:
                        pass
                
                files.append(info)
            except Exception:
                continue
        
        return files

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
                            "description": "Glob pattern to match (e.g., '*.py', 'test_*', 'config.*')."
                        },
                        "path": {
                            "type": "string",
                            "description": "Directory to search in (absolute path)."
                        },
                        "file_type": {
                            "type": "string",
                            "enum": ["file", "directory"],
                            "description": "Filter by type: 'file' or 'directory'. Default: both."
                        },
                        "extensions": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of extensions to include (e.g., ['py', 'js'])."
                        },
                        "max_depth": {
                            "type": "integer",
                            "description": "Maximum directory depth to search."
                        },
                        "include_hidden": {
                            "type": "boolean",
                            "description": "Include hidden files/directories. Default false.",
                            "default": False
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum results to return. Default 100.",
                            "default": 100
                        }
                    },
                    "required": ["pattern", "path"]
                }
            }
        }
