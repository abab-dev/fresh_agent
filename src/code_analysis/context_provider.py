"""
Context provider for extracting semantic context around code locations.

Given a file and line number, extracts the containing function/class/block.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from .symbol_extractor import SymbolExtractor, Symbol


@dataclass
class CodeContext:
    """Represents context around a code location."""
    file_path: str
    line: int
    type: str  # function, class, method, code_chunk
    name: str
    code: str
    line_start: int
    line_end: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "file": self.file_path,
            "target_line": self.line,
            "type": self.type,
            "name": self.name,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "code": self.code,
        }


class ContextProvider:
    """Provides semantic context around code locations."""
    
    _file_cache: Dict[str, tuple] = {}  # path -> (mtime, content, lines)
    _symbol_cache: Dict[str, List[Symbol]] = {}  # path -> symbols
    
    def __init__(self, cache_size: int = 100):
        self._cache_size = cache_size
    
    def _read_file(self, file_path: str) -> tuple:
        """Read file with caching based on mtime."""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            mtime = path.stat().st_mtime
        except OSError:
            raise
        
        cache_key = str(path.resolve())
        
        if cache_key in self._file_cache:
            cached_mtime, content, lines = self._file_cache[cache_key]
            if cached_mtime == mtime:
                return content, lines
        
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        lines = content.split("\n")
        
        if len(self._file_cache) >= self._cache_size:
            oldest_key = next(iter(self._file_cache))
            del self._file_cache[oldest_key]
        
        self._file_cache[cache_key] = (mtime, content, lines)
        return content, lines
    
    def _get_symbols(self, file_path: str, content: str) -> List[Symbol]:
        """Get symbols for a file with caching."""
        path = Path(file_path)
        cache_key = str(path.resolve())
        
        try:
            mtime = path.stat().st_mtime
        except OSError:
            mtime = 0
        
        if cache_key in self._symbol_cache:
            return self._symbol_cache[cache_key]
        
        symbols = SymbolExtractor.extract_symbols(file_path, content)
        
        if len(self._symbol_cache) >= self._cache_size:
            oldest_key = next(iter(self._symbol_cache))
            del self._symbol_cache[oldest_key]
        
        self._symbol_cache[cache_key] = symbols
        return symbols
    
    def get_context_around_line(
        self, 
        file_path: str, 
        line: int,
        context_lines: int = 10
    ) -> Optional[CodeContext]:
        """
        Get the semantic context (function/class) containing a specific line.
        
        Args:
            file_path: Path to the source file
            line: Line number (1-indexed)
            context_lines: Fallback context lines if no symbol contains the line
            
        Returns:
            CodeContext object with the containing scope, or None if not found
        """
        try:
            content, lines = self._read_file(file_path)
        except (FileNotFoundError, OSError):
            return None
        
        if line < 1 or line > len(lines):
            return None
        
        symbols = self._get_symbols(file_path, content)
        
        containing_symbol = None
        min_span = float("inf")
        
        for symbol in symbols:
            if symbol.line_start <= line <= symbol.line_end:
                span = symbol.line_end - symbol.line_start
                if span < min_span:
                    min_span = span
                    containing_symbol = symbol
        
        if containing_symbol:
            return CodeContext(
                file_path=file_path,
                line=line,
                type=containing_symbol.type,
                name=containing_symbol.name,
                code=containing_symbol.code,
                line_start=containing_symbol.line_start,
                line_end=containing_symbol.line_end,
            )
        
        start_idx = max(0, line - 1 - context_lines)
        end_idx = min(len(lines), line + context_lines)
        
        code = "\n".join(lines[start_idx:end_idx])
        
        return CodeContext(
            file_path=file_path,
            line=line,
            type="code_chunk",
            name=f"{Path(file_path).name}:{line}",
            code=code,
            line_start=start_idx + 1,
            line_end=end_idx,
        )
    
    def get_symbol_at_line(self, file_path: str, line: int) -> Optional[Symbol]:
        """Get the symbol defined at or containing a specific line."""
        try:
            content, _ = self._read_file(file_path)
        except (FileNotFoundError, OSError):
            return None
        
        symbols = self._get_symbols(file_path, content)
        
        for symbol in symbols:
            if symbol.line_start == line:
                return symbol
        
        containing = None
        min_span = float("inf")
        
        for symbol in symbols:
            if symbol.line_start <= line <= symbol.line_end:
                span = symbol.line_end - symbol.line_start
                if span < min_span:
                    min_span = span
                    containing = symbol
        
        return containing
    
    def invalidate_cache(self, file_path: Optional[str] = None):
        """Clear cache for a specific file or all files."""
        if file_path:
            cache_key = str(Path(file_path).resolve())
            self._file_cache.pop(cache_key, None)
            self._symbol_cache.pop(cache_key, None)
        else:
            self._file_cache.clear()
            self._symbol_cache.clear()
