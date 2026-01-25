from pathlib import Path
from typing import Optional, List, Tuple
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Replace specific text patterns in a file with fuzzy matching.

Use this for targeted edits where you want to:
- Change specific function names, variables, or strings
- Update configuration values
- Fix typos or make small corrections

The tool uses smart matching:
1. First tries exact match
2. Falls back to whitespace-normalized matching (ignores extra spaces)
3. Falls back to line-trimmed matching (ignores leading/trailing whitespace per line)

This handles minor whitespace differences that often cause edit failures."""


def find_match(content: str, search: str) -> Tuple[Optional[str], str]:
    """
    Find the best match for search string in content.
    
    Returns (matched_string, match_type) where match_type is:
    - "exact": exact match found
    - "whitespace": matched after normalizing whitespace
    - "line_trimmed": matched after trimming lines
    - "not_found": no match
    """
    # 1. Try exact match first
    if search in content:
        return search, "exact"
    
    # 2. Try whitespace-normalized matching
    normalized_search = ' '.join(search.split())
    content_lines = content.split('\n')
    search_lines = search.split('\n')
    
    # Single line whitespace match
    if len(search_lines) == 1:
        for line in content_lines:
            if ' '.join(line.split()) == normalized_search:
                return line, "whitespace"
    
    # Multi-line whitespace match
    if len(search_lines) > 1:
        for i in range(len(content_lines) - len(search_lines) + 1):
            block = content_lines[i:i + len(search_lines)]
            block_normalized = ' '.join('\n'.join(block).split())
            if block_normalized == normalized_search:
                return '\n'.join(block), "whitespace"
    
    # 3. Try line-trimmed matching (each line trimmed independently)
    search_trimmed = [line.strip() for line in search_lines]
    
    for i in range(len(content_lines) - len(search_lines) + 1):
        block = content_lines[i:i + len(search_lines)]
        block_trimmed = [line.strip() for line in block]
        
        if block_trimmed == search_trimmed:
            return '\n'.join(block), "line_trimmed"
    
    return None, "not_found"


class SearchReplaceTool(BaseTool):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_tool_name():
        return "search_replace"

    async def act(
        self, 
        file_path: str, 
        search: str, 
        replace: str, 
        replace_all: bool = False
    ):
        path = Path(file_path)
        
        if not path.exists():
            return {"error": f"File not found: {file_path}"}
        
        if not path.is_file():
            return {"error": f"Not a file: {file_path}"}
        
        try:
            content = path.read_text(encoding="utf-8")
            
            # Find match using fuzzy matching
            matched, match_type = find_match(content, search)
            
            if matched is None:
                return {
                    "error": "Search pattern not found in file",
                    "hint": "Check for whitespace differences. The search string must match the file content."
                }
            
            # Count occurrences of the matched string
            count = content.count(matched)
            
            if replace_all:
                new_content = content.replace(matched, replace)
                replaced_count = count
            else:
                if count > 1:
                    return {
                        "error": f"Found {count} occurrences. Provide more context to uniquely identify the target, or set replace_all=true.",
                        "match_type": match_type
                    }
                new_content = content.replace(matched, replace, 1)
                replaced_count = 1
            
            path.write_text(new_content, encoding="utf-8")
            
            result = {
                "result": f"Replaced {replaced_count} occurrence(s) in {file_path}",
                "total_matches": count,
                "replaced": replaced_count,
                "match_type": match_type
            }
            
            if match_type != "exact":
                result["note"] = f"Used {match_type} matching (original search had whitespace differences)"
            
            return result
            
        except PermissionError:
            return {"error": f"Permission denied: {file_path}"}
        except Exception as e:
            return {"error": f"Failed to search/replace: {str(e)}"}

    def json_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.get_tool_name(),
                "description": TOOL_DESCRIPTION,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The absolute path to the file to modify."
                        },
                        "search": {
                            "type": "string",
                            "description": "The text to search for. Fuzzy matching handles minor whitespace differences."
                        },
                        "replace": {
                            "type": "string",
                            "description": "The text to replace the search pattern with."
                        },
                        "replace_all": {
                            "type": "boolean",
                            "description": "Replace all occurrences (true) or just the first (false). Default false.",
                            "default": False
                        }
                    },
                    "required": ["file_path", "search", "replace"]
                }
            }
        }

