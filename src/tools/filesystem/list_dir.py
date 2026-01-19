import os
from pathlib import Path
from typing import List, Dict, Any
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """List the contents of a directory.

Returns files and subdirectories with their types and sizes.
Use this to explore project structure, find files, and understand codebase layout.

Options:
- recursive: List contents of subdirectories too
- max_depth: Limit recursion depth
- include_hidden: Show files starting with '.'"""


class ListDirTool(BaseTool):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_tool_name():
        return "list_dir"

    async def act(
        self, 
        path: str, 
        recursive: bool = False,
        max_depth: int = 3,
        include_hidden: bool = False,
        max_items: int = 200
    ):
        target = Path(path)
        
        if not target.exists():
            return {"error": f"Path not found: {path}"}
        
        if not target.is_dir():
            return {"error": f"Not a directory: {path}"}
        
        try:
            items = []
            self._list_directory(
                target, 
                items, 
                recursive=recursive,
                max_depth=max_depth,
                current_depth=0,
                include_hidden=include_hidden,
                max_items=max_items,
                base_path=target
            )
            
            truncated = len(items) >= max_items
            
            return {
                "path": str(target),
                "items": items,
                "count": len(items),
                "truncated": truncated
            }
            
        except PermissionError:
            return {"error": f"Permission denied: {path}"}
        except Exception as e:
            return {"error": f"Failed to list directory: {str(e)}"}

    def _list_directory(
        self,
        directory: Path,
        items: List[Dict[str, Any]],
        recursive: bool,
        max_depth: int,
        current_depth: int,
        include_hidden: bool,
        max_items: int,
        base_path: Path
    ):
        if len(items) >= max_items:
            return
        
        try:
            entries = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        except PermissionError:
            return
        
        for entry in entries:
            if len(items) >= max_items:
                return
            
            if not include_hidden and entry.name.startswith('.'):
                continue
            
            try:
                rel_path = entry.relative_to(base_path)
                item = {
                    "name": str(rel_path),
                    "type": "dir" if entry.is_dir() else "file"
                }
                
                if entry.is_file():
                    item["size"] = entry.stat().st_size
                
                items.append(item)
                
                if recursive and entry.is_dir() and current_depth < max_depth:
                    self._list_directory(
                        entry,
                        items,
                        recursive=recursive,
                        max_depth=max_depth,
                        current_depth=current_depth + 1,
                        include_hidden=include_hidden,
                        max_items=max_items,
                        base_path=base_path
                    )
            except (PermissionError, OSError):
                continue

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
                            "description": "The absolute path to the directory to list."
                        },
                        "recursive": {
                            "type": "boolean",
                            "description": "List subdirectories recursively. Default false.",
                            "default": False
                        },
                        "max_depth": {
                            "type": "integer",
                            "description": "Maximum recursion depth. Default 3.",
                            "default": 3
                        },
                        "include_hidden": {
                            "type": "boolean",
                            "description": "Include hidden files (starting with '.'). Default false.",
                            "default": False
                        }
                    },
                    "required": ["path"]
                }
            }
        }
