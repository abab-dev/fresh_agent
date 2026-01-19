import asyncio
import os
import fnmatch
from pathlib import Path
from typing import Optional, List
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Search for files by name or pattern.

Useful for:
- Finding files by name (e.g., 'config.py', 'package.json')
- Locating files matching a pattern (e.g., '*.test.js', '*_spec.py')
- Discovering project structure and file organization

Returns file paths matching the pattern within the search directory."""


class FileSearchTool(BaseTool):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_tool_name():
        return "file_search"

    async def act(
        self,
        pattern: str,
        path: str,
        max_results: int = 50,
        include_hidden: bool = False
    ):
        search_path = Path(path)
        
        if not search_path.exists():
            return {"error": f"Path not found: {path}"}
        
        if not search_path.is_dir():
            return {"error": f"Not a directory: {path}"}
        
        try:
            matches = []
            skip_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv", ".tox", ".pytest_cache"}
            
            for root, dirs, files in os.walk(search_path):
                dirs[:] = [d for d in dirs if d not in skip_dirs]
                if not include_hidden:
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for filename in files:
                    if not include_hidden and filename.startswith('.'):
                        continue
                    
                    if fnmatch.fnmatch(filename, pattern) or fnmatch.fnmatch(filename.lower(), pattern.lower()):
                        full_path = os.path.join(root, filename)
                        try:
                            size = os.path.getsize(full_path)
                            matches.append({
                                "path": full_path,
                                "name": filename,
                                "size": size
                            })
                        except OSError:
                            matches.append({
                                "path": full_path,
                                "name": filename
                            })
                    
                    if len(matches) >= max_results:
                        break
                
                if len(matches) >= max_results:
                    break
            
            truncated = len(matches) >= max_results
            
            return {
                "result": f"Found {len(matches)} file(s)",
                "files": matches,
                "truncated": truncated
            }
            
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
                            "description": "The filename pattern to search for (supports wildcards like *.py)."
                        },
                        "path": {
                            "type": "string",
                            "description": "The directory to search in."
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results. Default 50.",
                            "default": 50
                        },
                        "include_hidden": {
                            "type": "boolean",
                            "description": "Include hidden files and directories. Default false.",
                            "default": False
                        }
                    },
                    "required": ["pattern", "path"]
                }
            }
        }
