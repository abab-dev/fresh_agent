"""
Repository mapper for building file trees and symbol maps.

Provides a complete structural overview of a codebase.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass

from .symbol_extractor import SymbolExtractor


IGNORED_DIRS = {
    ".git", ".svn", ".hg", ".bzr",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "node_modules", ".next", "dist", "build",
    ".venv", "venv", ".env", ".tox",
    "target",  # Rust/Java
    "vendor",  # Go/PHP
    "deps", "_build",  # Elixir
    ".idea", ".vscode",
    "coverage", ".coverage",
}


@dataclass
class FileInfo:
    path: str  # relative to repo root
    size: int
    is_file: bool
    language: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "path": self.path,
            "size": self.size,
            "is_file": self.is_file,
        }
        if self.language:
            result["language"] = self.language
        return result


class RepoMapper:
    """Maps repository structure and symbols."""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path).resolve()
        self._symbol_cache: Dict[str, List[Dict[str, Any]]] = {}
        self._scanned = False
    
    def _should_ignore(self, path: Path) -> bool:
        """Check if a path should be ignored."""
        name = path.name
        
        if name.startswith(".") and name not in {".github", ".gitlab"}:
            if path.is_dir():
                return True
        
        if path.is_dir() and name in IGNORED_DIRS:
            return True
        
        return False
    
    def get_file_tree(
        self, 
        subpath: Optional[str] = None,
        include_hidden: bool = False,
        max_files: int = 5000
    ) -> List[Dict[str, Any]]:
        """
        Get the file tree of the repository.
        
        Args:
            subpath: Optional subdirectory to start from
            include_hidden: Include hidden files/directories
            max_files: Maximum number of files to return
            
        Returns:
            List of file info dicts
        """
        start_path = self.repo_path
        if subpath:
            start_path = self.repo_path / subpath
            if not start_path.exists():
                return []
        
        files = []
        
        for root, dirs, filenames in os.walk(start_path):
            root_path = Path(root)
            
            if not include_hidden:
                dirs[:] = [d for d in dirs if not self._should_ignore(root_path / d)]
            
            for filename in filenames:
                if len(files) >= max_files:
                    break
                
                file_path = root_path / filename
                
                if not include_hidden and filename.startswith("."):
                    continue
                
                try:
                    rel_path = file_path.relative_to(self.repo_path)
                    size = file_path.stat().st_size
                    language = SymbolExtractor.get_language(str(file_path))
                    
                    files.append(FileInfo(
                        path=str(rel_path),
                        size=size,
                        is_file=True,
                        language=language
                    ))
                except (OSError, ValueError):
                    continue
            
            if len(files) >= max_files:
                break
        
        return [f.to_dict() for f in files]
    
    def scan_symbols(
        self, 
        subpath: Optional[str] = None,
        extensions: Optional[Set[str]] = None,
        max_files: int = 1000
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Scan repository for symbols in all supported files.
        
        Args:
            subpath: Optional subdirectory to scan
            extensions: Limit to specific extensions (e.g., {".py", ".js"})
            max_files: Maximum files to scan
            
        Returns:
            Dict mapping file paths to their symbols
        """
        start_path = self.repo_path
        if subpath:
            start_path = self.repo_path / subpath
        
        symbols_map = {}
        files_scanned = 0
        
        for root, dirs, filenames in os.walk(start_path):
            root_path = Path(root)
            
            dirs[:] = [d for d in dirs if not self._should_ignore(root_path / d)]
            
            for filename in filenames:
                if files_scanned >= max_files:
                    break
                
                file_path = root_path / filename
                
                if filename.startswith("."):
                    continue
                
                if not SymbolExtractor.is_supported(str(file_path)):
                    continue
                
                if extensions:
                    ext = file_path.suffix.lower()
                    if ext not in extensions:
                        continue
                
                try:
                    rel_path = str(file_path.relative_to(self.repo_path))
                    symbols = SymbolExtractor.extract_symbols_dict(str(file_path))
                    
                    if symbols:
                        symbols_map[rel_path] = symbols
                        files_scanned += 1
                except (OSError, ValueError):
                    continue
            
            if files_scanned >= max_files:
                break
        
        self._symbol_cache = symbols_map
        self._scanned = True
        
        return symbols_map
    
    def get_repo_structure(
        self,
        scan_symbols: bool = True,
        max_files: int = 1000
    ) -> Dict[str, Any]:
        """
        Get complete repository structure including files and symbols.
        
        Returns:
            Dict with file tree, symbols, and statistics
        """
        files = self.get_file_tree(max_files=max_files * 2)
        
        if scan_symbols:
            symbols = self.scan_symbols(max_files=max_files)
        else:
            symbols = self._symbol_cache if self._scanned else {}
        
        languages: Dict[str, int] = {}
        for f in files:
            lang = f.get("language")
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
        
        total_symbols = sum(len(syms) for syms in symbols.values())
        
        return {
            "root": str(self.repo_path),
            "files": files,
            "symbols": symbols,
            "stats": {
                "total_files": len(files),
                "total_symbols": total_symbols,
                "files_with_symbols": len(symbols),
                "languages": languages,
            }
        }
    
    def get_file_symbols(self, file_path: str) -> List[Dict[str, Any]]:
        """Get symbols for a specific file."""
        path = Path(file_path)
        if not path.is_absolute():
            path = self.repo_path / path
        
        return SymbolExtractor.extract_symbols_dict(str(path))
    
    def find_symbol(
        self, 
        name: str, 
        symbol_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Find all symbols matching a name."""
        if not self._scanned:
            self.scan_symbols()
        
        matches = []
        for file_path, symbols in self._symbol_cache.items():
            for symbol in symbols:
                if symbol["name"] == name:
                    if symbol_type is None or symbol["type"] == symbol_type:
                        matches.append({
                            "file": file_path,
                            **symbol
                        })
        
        return matches
    
    def get_structure_summary(self) -> str:
        """Get a compact text summary of the repository structure."""
        structure = self.get_repo_structure(scan_symbols=True, max_files=500)
        
        lines = [
            f"Repository: {structure['root']}",
            f"Files: {structure['stats']['total_files']}",
            f"Symbols: {structure['stats']['total_symbols']}",
            "",
            "Languages:"
        ]
        
        for lang, count in sorted(structure['stats']['languages'].items(), key=lambda x: -x[1]):
            lines.append(f"  {lang}: {count} files")
        
        lines.append("")
        lines.append("Key files with symbols:")
        
        files_by_symbols = sorted(
            structure['symbols'].items(),
            key=lambda x: len(x[1]),
            reverse=True
        )[:20]
        
        for file_path, symbols in files_by_symbols:
            symbol_names = [s['name'] for s in symbols[:5]]
            extra = f" +{len(symbols)-5} more" if len(symbols) > 5 else ""
            lines.append(f"  {file_path}: {', '.join(symbol_names)}{extra}")
        
        return "\n".join(lines)
