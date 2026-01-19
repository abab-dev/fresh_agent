"""
Multi-language symbol extraction using tree-sitter queries.

Extracts functions, classes, methods with their signatures, line numbers,
and code content across Python, JavaScript, and TypeScript.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, ClassVar
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

try:
    import tree_sitter
    from tree_sitter_language_pack import get_parser, get_language
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False
    logger.warning("tree-sitter not installed. Symbol extraction will be limited.")


LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",  # TSX uses typescript queries
}

QUERIES_DIR = Path(__file__).parent / "queries"


@dataclass
class Symbol:
    name: str
    type: str  # function, class, method, interface, enum, type
    line_start: int
    line_end: int
    code: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "code": self.code,
        }


class SymbolExtractor:
    """Multi-language symbol extractor using tree-sitter queries."""
    
    _parsers: ClassVar[Dict[str, Any]] = {}
    _queries: ClassVar[Dict[str, Any]] = {}
    
    @classmethod
    def get_language(cls, file_path: str) -> Optional[str]:
        """Get language name from file extension."""
        ext = Path(file_path).suffix.lower()
        return LANGUAGE_MAP.get(ext)
    
    @classmethod
    def is_supported(cls, file_path: str) -> bool:
        """Check if file type is supported."""
        return cls.get_language(file_path) is not None and TREE_SITTER_AVAILABLE
    
    @classmethod
    def _get_parser(cls, lang_name: str):
        """Get or create parser for a language."""
        if not TREE_SITTER_AVAILABLE:
            return None
        if lang_name not in cls._parsers:
            try:
                cls._parsers[lang_name] = get_parser(lang_name)
            except Exception as e:
                logger.warning(f"Failed to get parser for {lang_name}: {e}")
                return None
        return cls._parsers[lang_name]
    
    @classmethod
    def _load_query(cls, lang_name: str) -> Optional[str]:
        """Load query file for a language."""
        query_file = QUERIES_DIR / lang_name / "tags.scm"
        if not query_file.exists():
            logger.warning(f"Query file not found: {query_file}")
            return None
        
        try:
            return query_file.read_text(encoding="utf-8")
        except IOError as e:
            logger.warning(f"Failed to read query file: {e}")
            return None
    
    @classmethod
    def _get_query(cls, lang_name: str):
        """Get or create query for a language."""
        if not TREE_SITTER_AVAILABLE:
            return None
        
        if lang_name in cls._queries:
            return cls._queries[lang_name]
        
        query_content = cls._load_query(lang_name)
        if not query_content:
            return None
        
        try:
            language = get_language(lang_name)
            query = tree_sitter.Query(language, query_content)
            cls._queries[lang_name] = query
            return query
        except tree_sitter.QueryError as e:
            logger.error(f"Query syntax error for {lang_name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to create query for {lang_name}: {e}")
            return None
    
    @classmethod
    def extract_symbols(cls, file_path: str, source_code: Optional[str] = None) -> List[Symbol]:
        """
        Extract symbols from a source file using tree-sitter queries.
        
        Args:
            file_path: Path to the file
            source_code: Optional source code (if not provided, reads from file)
            
        Returns:
            List of Symbol objects
        """
        lang_name = cls.get_language(file_path)
        if not lang_name:
            return []
        
        if source_code is None:
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    source_code = f.read()
            except (IOError, OSError) as e:
                logger.warning(f"Failed to read {file_path}: {e}")
                return []
        
        if not TREE_SITTER_AVAILABLE:
            return cls._extract_symbols_fallback(source_code, lang_name)
        
        return cls._extract_with_query(source_code, lang_name)
    
    @classmethod
    def _extract_with_query(cls, source_code: str, lang_name: str) -> List[Symbol]:
        """Extract symbols using tree-sitter query-based approach."""
        parser = cls._get_parser(lang_name)
        query = cls._get_query(lang_name)
        
        if not parser or not query:
            return []
        
        try:
            tree = parser.parse(source_code.encode("utf-8"))
            root = tree.root_node
        except Exception as e:
            logger.warning(f"Failed to parse code: {e}")
            return []
        
        symbols = []
        seen = set()  # For deduplication
        
        try:
            # Use QueryCursor API (tree-sitter >= 0.25.1)
            cursor = tree_sitter.QueryCursor(query)
            matches = list(cursor.matches(root))
            
            for pattern_index, captures in matches:
                symbol = cls._process_match(captures, source_code)
                if symbol:
                    # Deduplicate by (name, type, start, end)
                    key = (symbol.name, symbol.type, symbol.line_start, symbol.line_end)
                    if key not in seen:
                        seen.add(key)
                        symbols.append(symbol)
            
        except Exception as e:
            logger.error(f"Error processing matches: {e}")
            return []
        
        return symbols
    
    @classmethod
    def _process_match(cls, captures: Dict[str, Any], source_code: str) -> Optional[Symbol]:
        """Process a single query match and extract symbol info."""
        
        # Get the name node
        name_node = captures.get("name")
        if isinstance(name_node, list):
            name_node = name_node[0] if name_node else None
        if not name_node:
            return None
        
        # Extract symbol name
        symbol_name = name_node.text.decode("utf-8") if hasattr(name_node, "text") else str(name_node)
        
        # Find the definition capture to get symbol type and body
        definition_node = None
        symbol_type = "symbol"
        
        for capture_name, node in captures.items():
            if capture_name.startswith("definition."):
                symbol_type = capture_name.split(".")[-1]
                definition_node = node
                if isinstance(definition_node, list):
                    definition_node = definition_node[0] if definition_node else None
                break
        
        # Use definition node for line span and code, fall back to name node
        body_node = definition_node or name_node
        
        if not body_node:
            return None
        
        line_start = body_node.start_point[0] + 1  # 1-indexed
        line_end = body_node.end_point[0] + 1
        
        # Extract code content
        if hasattr(body_node, "text") and isinstance(body_node.text, bytes):
            code = body_node.text.decode("utf-8", errors="ignore")
        elif hasattr(body_node, "start_byte") and hasattr(body_node, "end_byte"):
            code = source_code[body_node.start_byte:body_node.end_byte]
        else:
            code = symbol_name
        
        return Symbol(
            name=symbol_name,
            type=symbol_type,
            line_start=line_start,
            line_end=line_end,
            code=code
        )
    
    @classmethod
    def _extract_symbols_fallback(cls, source_code: str, lang_name: str) -> List[Symbol]:
        """Fallback extraction using regex when tree-sitter is not available."""
        import re
        symbols = []
        lines = source_code.split("\n")
        
        if lang_name == "python":
            for i, line in enumerate(lines):
                func_match = re.match(r"^(\s*)(?:async\s+)?def\s+(\w+)\s*\(", line)
                if func_match:
                    indent = len(func_match.group(1))
                    name = func_match.group(2)
                    symbols.append(Symbol(
                        name=name,
                        type="function" if indent == 0 else "method",
                        line_start=i + 1,
                        line_end=i + 1,
                        code=line.strip()
                    ))
                
                class_match = re.match(r"^\s*class\s+(\w+)", line)
                if class_match:
                    name = class_match.group(1)
                    symbols.append(Symbol(
                        name=name,
                        type="class",
                        line_start=i + 1,
                        line_end=i + 1,
                        code=line.strip()
                    ))
        
        elif lang_name in ("javascript", "typescript"):
            for i, line in enumerate(lines):
                func_match = re.match(r"^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)", line)
                if func_match:
                    symbols.append(Symbol(
                        name=func_match.group(1),
                        type="function",
                        line_start=i + 1,
                        line_end=i + 1,
                        code=line.strip()
                    ))
                
                class_match = re.match(r"^\s*(?:export\s+)?class\s+(\w+)", line)
                if class_match:
                    symbols.append(Symbol(
                        name=class_match.group(1),
                        type="class",
                        line_start=i + 1,
                        line_end=i + 1,
                        code=line.strip()
                    ))
                
                arrow_match = re.match(r"^\s*(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(", line)
                if arrow_match:
                    symbols.append(Symbol(
                        name=arrow_match.group(1),
                        type="function",
                        line_start=i + 1,
                        line_end=i + 1,
                        code=line.strip()
                    ))
        
        return symbols
    
    @classmethod
    def extract_symbols_dict(cls, file_path: str, source_code: Optional[str] = None) -> List[Dict[str, Any]]:
        """Extract symbols and return as list of dicts."""
        symbols = cls.extract_symbols(file_path, source_code)
        return [s.to_dict() for s in symbols]
