"""
Simplified glob-based file finder.

Based on RepOMind's glob_search - minimal parameters, maximum clarity.
"""

import asyncio
import os
import shutil
from pathlib import Path
from typing import Optional, List
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Find files matching a glob pattern.

Fast file discovery using fd (falls back to find).

Args:
    pattern: Glob pattern (e.g., '*.py', 'test_*', '**/*config*')
    path: Directory to search (default: workspace root)

Use cases:
- Find all Python files: *.py
- Find test files: test_*.py or *_test.py
- Find config files: *config* or *.json
- Find by partial name: *auth*, *api*"""


class GlobTool(BaseTool):
    def __init__(self, workspace_root: str = None):
        super().__init__()
        self._has_fd = shutil.which("fd") is not None
        self._workspace_root = workspace_root or os.getcwd()

    @staticmethod
    def get_tool_name():
        return "glob"

    def _resolve_path(self, path: Optional[str]) -> str:
        """Resolve path to absolute. Default to workspace root."""
        if path is None:
            return self._workspace_root
        
        if not os.path.isabs(path):
            return os.path.join(self._workspace_root, path)
        
        return path

    async def act(
        self,
        pattern: str,
        path: Optional[str] = None
    ):
        """
        Find files matching a pattern.
        
        Args:
            pattern: Glob pattern (e.g., '*.py', 'test_*', '*config*')
            path: Directory to search (default: workspace root)
        """
        search_path = self._resolve_path(path)
        
        if not os.path.exists(search_path):
            return {"error": f"Path not found: {search_path}"}
        
        if not os.path.isdir(search_path):
            return {"error": f"Not a directory: {search_path}"}
        
        if self._has_fd:
            return await self._search_fd(pattern, search_path)
        else:
            return await self._search_find(pattern, search_path)

    async def _search_fd(self, pattern: str, path: str):
        cmd = ["fd", "--type", "f", "--full-path", "--glob", "--max-results", "100", "--", pattern, path]
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, _ = await asyncio.wait_for(process.communicate(), timeout=30)
            output = stdout.decode("utf-8", errors="replace")
            files = self._parse_results(output, path)
            
            return {
                "result": f"Found {len(files)} files",
                "files": files,
                "truncated": len(files) >= 100,
                "engine": "fd"
            }
            
        except asyncio.TimeoutError:
            return {"error": "Search timed out"}
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

    async def _search_find(self, pattern: str, path: str):
        cmd = ["find", path, "-type", "f", "-name", pattern]
        
        # Exclude common directories
        for exc in [".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"]:
            cmd.extend(["-not", "-path", f"*/{exc}/*"])
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, _ = await asyncio.wait_for(process.communicate(), timeout=30)
            output = stdout.decode("utf-8", errors="replace")
            files = self._parse_results(output, path)
            
            return {
                "result": f"Found {len(files)} files",
                "files": files,
                "truncated": len(files) >= 100,
                "engine": "find"
            }
            
        except asyncio.TimeoutError:
            return {"error": "Search timed out"}
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

    def _parse_results(self, output: str, base_path: str) -> List[dict]:
        files = []
        base = Path(base_path).resolve()
        
        for line in output.strip().split("\n")[:100]:
            if not line:
                continue
            
            try:
                full_path = Path(line.strip()).resolve()
                
                try:
                    rel_path = full_path.relative_to(base)
                except ValueError:
                    rel_path = full_path
                
                files.append({
                    "path": str(full_path),
                    "name": full_path.name
                })
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
                            "description": "Glob pattern to match (e.g., '*.py', 'test_*', '*config*')."
                        },
                        "path": {
                            "type": "string",
                            "description": "Directory to search. Default: workspace root."
                        }
                    },
                    "required": ["pattern"]
                }
            }
        }
