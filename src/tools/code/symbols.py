import os
from typing import Optional, List
from src.tools.base import BaseTool
from src.code_analysis.symbol_extractor import SymbolExtractor
from src.code_analysis.repo_mapper import RepoMapper


TOOL_DESCRIPTION = """Extract symbols (functions, classes, methods) from source code files.

Use this to understand code structure without reading entire files:
- List all functions/classes in a file
- See function signatures and docstrings
- Scan a directory for all symbols

Supports: Python, JavaScript, TypeScript, Go, Rust, Java, C/C++, Ruby, and more.

Returns structured data with name, type, line numbers, signatures, and docstrings."""


class ExtractSymbolsTool(BaseTool):
    def __init__(self):
        super().__init__()
        self._mapper = None

    @staticmethod
    def get_tool_name():
        return "extract_symbols"

    def _get_mapper(self, path: str) -> RepoMapper:
        # Determine repo root from path
        check_path = os.path.abspath(path)
        if os.path.isfile(check_path):
            check_path = os.path.dirname(check_path)
        
        # Walk up to find .git or use cwd
        while check_path != "/":
            if os.path.exists(os.path.join(check_path, ".git")):
                break
            check_path = os.path.dirname(check_path)
        
        if check_path == "/":
            check_path = os.getcwd()
        
        return RepoMapper(check_path)

    async def act(
        self,
        path: str,
        recursive: bool = False,
        symbol_type: Optional[str] = None,
        max_files: int = 100
    ):
        """
        Extract symbols from a file or directory.
        
        Args:
            path: File or directory path (absolute)
            recursive: For directories, scan recursively
            symbol_type: Filter by type (function, class, method)
            max_files: Maximum files to scan for directories
        """
        if not os.path.exists(path):
            return {"error": f"Path not found: {path}"}
        
        if os.path.isfile(path):
            # Single file
            if not SymbolExtractor.is_supported(path):
                return {
                    "error": f"Unsupported file type. Supported: Python, JS/TS, Go, Rust, Java, C/C++, Ruby, etc."
                }
            
            symbols = SymbolExtractor.extract_symbols_dict(path)
            
            if symbol_type:
                symbols = [s for s in symbols if s.get("type") == symbol_type]
            
            return {
                "file": path,
                "symbol_count": len(symbols),
                "symbols": symbols
            }
        
        else:
            # Directory
            mapper = self._get_mapper(path)
            
            # Get relative subpath if path is within repo
            try:
                subpath = os.path.relpath(path, mapper.repo_path)
                if subpath == ".":
                    subpath = None
            except ValueError:
                subpath = None
            
            symbols_map = mapper.scan_symbols(subpath=subpath, max_files=max_files)
            
            # Flatten and optionally filter
            all_symbols = []
            for file_path, symbols in symbols_map.items():
                for symbol in symbols:
                    if symbol_type is None or symbol.get("type") == symbol_type:
                        all_symbols.append({
                            "file": file_path,
                            **symbol
                        })
            
            return {
                "path": path,
                "files_scanned": len(symbols_map),
                "symbol_count": len(all_symbols),
                "symbols": all_symbols[:500]  # Limit output size
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
                            "description": "Absolute path to file or directory to extract symbols from."
                        },
                        "recursive": {
                            "type": "boolean",
                            "description": "For directories, scan subdirectories recursively. Default true.",
                            "default": True
                        },
                        "symbol_type": {
                            "type": "string",
                            "enum": ["function", "class", "method"],
                            "description": "Filter results by symbol type."
                        },
                        "max_files": {
                            "type": "integer",
                            "description": "Maximum files to scan in directory mode. Default 100.",
                            "default": 100
                        }
                    },
                    "required": ["path"]
                }
            }
        }
