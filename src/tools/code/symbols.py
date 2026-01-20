"""
Simplified symbol extraction tool.

Extract function/class definitions from source code files.
"""

import os
from typing import Optional
from src.tools.base import BaseTool
from src.code_analysis.symbol_extractor import SymbolExtractor
from src.code_analysis.repo_mapper import RepoMapper


TOOL_DESCRIPTION = """Extract function/class definitions from source code.

Use this to understand code structure without reading entire files.

Args:
    path: File or directory to analyze (absolute path)

Supports: Python, JavaScript, TypeScript, Go, Rust, Java, C/C++, Ruby."""


class ExtractSymbolsTool(BaseTool):
    def __init__(self, workspace_root: str = None):
        super().__init__()
        self._workspace_root = workspace_root or os.getcwd()
        self._mapper = None

    @staticmethod
    def get_tool_name():
        return "extract_symbols"

    def _resolve_path(self, path: Optional[str]) -> str:
        """Resolve path to absolute. Default to workspace root."""
        if path is None:
            return self._workspace_root
        
        if not os.path.isabs(path):
            return os.path.join(self._workspace_root, path)
        
        return path

    def _get_mapper(self, path: str) -> RepoMapper:
        check_path = os.path.abspath(path)
        if os.path.isfile(check_path):
            check_path = os.path.dirname(check_path)
        
        while check_path != "/":
            if os.path.exists(os.path.join(check_path, ".git")):
                break
            check_path = os.path.dirname(check_path)
        
        if check_path == "/":
            check_path = self._workspace_root
        
        return RepoMapper(check_path)

    async def act(self, path: str):
        """
        Extract symbols from a file or directory.
        
        Args:
            path: File or directory path (absolute)
        """
        resolved_path = self._resolve_path(path)
        
        if not os.path.exists(resolved_path):
            return {"error": f"Path not found: {resolved_path}"}
        
        if os.path.isfile(resolved_path):
            if not SymbolExtractor.is_supported(resolved_path):
                return {"error": "Unsupported file type"}
            
            symbols = SymbolExtractor.extract_symbols_dict(resolved_path)
            return {
                "file": resolved_path,
                "symbol_count": len(symbols),
                "symbols": symbols
            }
        
        else:
            mapper = self._get_mapper(resolved_path)
            
            try:
                subpath = os.path.relpath(resolved_path, mapper.repo_path)
                if subpath == ".":
                    subpath = None
            except ValueError:
                subpath = None
            
            symbols_map = mapper.scan_symbols(subpath=subpath, max_files=100)
            
            all_symbols = []
            for file_path, symbols in symbols_map.items():
                for symbol in symbols:
                    all_symbols.append({
                        "file": file_path,
                        **symbol
                    })
            
            return {
                "path": resolved_path,
                "files_scanned": len(symbols_map),
                "symbol_count": len(all_symbols),
                "symbols": all_symbols[:500]
            }

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
                            "description": "Absolute path to file or directory."
                        }
                    },
                    "required": ["path"]
                }
            }
        }
