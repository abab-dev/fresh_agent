import os
import json
from pathlib import Path
from typing import Optional
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """List stored memories.

Retrieve previously saved memories with optional filtering:
- Filter by category
- Filter by tags
- Limit number of results

Use this to recall important context from previous sessions."""


MEMORY_FILE = ".agent_memory.json"


class ListMemoriesTool(BaseTool):
    def __init__(self, memory_path: str = None):
        super().__init__()
        self._memory_path = memory_path or os.path.join(os.getcwd(), MEMORY_FILE)

    @staticmethod
    def get_tool_name():
        return "list_memories"

    async def act(
        self,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 20
    ):
        try:
            memories = self._load_memories()
            
            if not memories:
                return {"result": "No memories found", "memories": []}
            
            filtered = memories
            
            if category:
                filtered = [m for m in filtered if m.get("category") == category]
            
            if tag:
                filtered = [m for m in filtered if tag in m.get("tags", [])]
            
            filtered = filtered[-limit:]
            
            return {
                "result": f"Found {len(filtered)} memories",
                "memories": filtered,
                "total": len(memories)
            }
            
        except Exception as e:
            return {"error": f"Failed to list memories: {str(e)}"}

    def _load_memories(self) -> list:
        path = Path(self._memory_path)
        if not path.exists():
            return []
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def json_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.get_tool_name(),
                "description": TOOL_DESCRIPTION,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "Filter by memory category."
                        },
                        "tag": {
                            "type": "string",
                            "description": "Filter by tag."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of memories to return. Default 20.",
                            "default": 20
                        }
                    },
                    "required": []
                }
            }
        }
