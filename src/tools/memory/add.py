import os
import json
from datetime import datetime
from pathlib import Path
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Store a memory note for future reference.

Use this to persist important information across sessions:
- User preferences and coding style
- Project-specific conventions and decisions
- Important context that should be remembered

Memories are stored in a local JSON file and can be retrieved later."""


MEMORY_FILE = ".agent_memory.json"


class AddMemoryTool(BaseTool):
    def __init__(self, memory_path: str = None):
        super().__init__()
        self._memory_path = memory_path or os.path.join(os.getcwd(), MEMORY_FILE)

    @staticmethod
    def get_tool_name():
        return "add_memory"

    async def act(self, content: str, category: str = "general", tags: list = None):
        if not content or not content.strip():
            return {"error": "Memory content is required"}
        
        try:
            memories = self._load_memories()
            
            memory_id = f"mem_{len(memories)}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            memory = {
                "id": memory_id,
                "content": content.strip(),
                "category": category,
                "tags": tags or [],
                "created_at": datetime.now().isoformat()
            }
            
            memories.append(memory)
            self._save_memories(memories)
            
            return {
                "result": "Memory saved",
                "id": memory_id,
                "total_memories": len(memories)
            }
            
        except Exception as e:
            return {"error": f"Failed to save memory: {str(e)}"}

    def _load_memories(self) -> list:
        path = Path(self._memory_path)
        if not path.exists():
            return []
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_memories(self, memories: list):
        with open(self._memory_path, "w", encoding="utf-8") as f:
            json.dump(memories, f, indent=2, ensure_ascii=False)

    def json_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.get_tool_name(),
                "description": TOOL_DESCRIPTION,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "The memory content to store."
                        },
                        "category": {
                            "type": "string",
                            "description": "Category for the memory (e.g., 'preference', 'decision', 'context'). Default 'general'.",
                            "default": "general"
                        },
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional tags for easier retrieval."
                        }
                    },
                    "required": ["content"]
                }
            }
        }
