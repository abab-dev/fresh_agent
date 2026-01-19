import os
from typing import Optional
from src.tools.base import BaseTool
from src.code_analysis.repo_mapper import RepoMapper


TOOL_DESCRIPTION = """Get an overview of a repository or directory structure.

Returns:
- File tree with languages detected
- All extracted symbols (functions, classes, methods)
- Statistics: file counts, symbol counts, language breakdown

Use this as a first step when exploring a new codebase to understand:
- What languages are used
- Key files and their main symbols
- Overall project structure

Much faster than reading individual files to understand a project."""


class RepoStructureTool(BaseTool):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_tool_name():
        return "repo_structure"

    async def act(
        self,
        path: str,
        scan_symbols: bool = True,
        max_files: int = 200,
        summary_only: bool = False
    ):
        """
        Get repository structure and symbols.
        
        Args:
            path: Path to repository or directory (absolute)
            scan_symbols: Whether to extract symbols from files
            max_files: Maximum files to scan for symbols
            summary_only: Return compact text summary instead of full data
        """
        if not os.path.exists(path):
            return {"error": f"Path not found: {path}"}
        
        if not os.path.isdir(path):
            return {"error": f"Not a directory: {path}"}
        
        mapper = RepoMapper(path)
        
        if summary_only:
            summary = mapper.get_structure_summary()
            return {
                "path": path,
                "summary": summary
            }
        
        structure = mapper.get_repo_structure(
            scan_symbols=scan_symbols,
            max_files=max_files
        )
        
        # Simplify symbols for output
        simplified_symbols = {}
        for file_path, symbols in structure["symbols"].items():
            simplified_symbols[file_path] = [
                {
                    "name": s["name"],
                    "type": s["type"],
                    "line": s.get("line_start"),
                    "signature": s.get("signature", "")[:100]
                }
                for s in symbols
            ]
        
        return {
            "path": structure["root"],
            "stats": structure["stats"],
            "files": structure["files"][:500],  # Limit file list
            "symbols": simplified_symbols
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
                            "description": "Absolute path to the repository or directory."
                        },
                        "scan_symbols": {
                            "type": "boolean",
                            "description": "Whether to extract symbols from source files. Default true.",
                            "default": True
                        },
                        "max_files": {
                            "type": "integer",
                            "description": "Maximum files to scan for symbols. Default 200.",
                            "default": 200
                        },
                        "summary_only": {
                            "type": "boolean",
                            "description": "Return compact text summary instead of full data. Default false.",
                            "default": False
                        }
                    },
                    "required": ["path"]
                }
            }
        }
