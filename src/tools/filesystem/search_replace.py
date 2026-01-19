from pathlib import Path
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Replace specific text patterns in a file.

Use this for targeted edits where you want to:
- Change specific function names, variables, or strings
- Update configuration values
- Fix typos or make small corrections

The tool finds and replaces the first occurrence of the search pattern.
Use with caution - verify the search pattern is unique in the file."""


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
            
            if search not in content:
                return {"error": f"Search pattern not found in file"}
            
            count = content.count(search)
            
            if replace_all:
                new_content = content.replace(search, replace)
                replaced_count = count
            else:
                new_content = content.replace(search, replace, 1)
                replaced_count = 1
            
            path.write_text(new_content, encoding="utf-8")
            
            return {
                "result": f"Replaced {replaced_count} occurrence(s) in {file_path}",
                "total_matches": count,
                "replaced": replaced_count
            }
            
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
                            "description": "The exact text to search for."
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
