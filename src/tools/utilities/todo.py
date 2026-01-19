import os
from pathlib import Path
from datetime import datetime
from typing import Literal, Optional, Protocol
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Manage a todo list for tracking task progress.

Actions:
- add: Add a new todo item
- complete: Mark a todo as completed
- list: Show all todos
- clear: Remove all completed todos

Use this to break down complex tasks and track progress.
Creates a todo.md file in the current directory."""


class UIProtocol(Protocol):
    def print_info(self, message: str) -> None: ...


class TodoTool(BaseTool):
    def __init__(self, ui_manager: Optional[UIProtocol] = None, todo_path: str = None):
        super().__init__()
        self._ui_manager = ui_manager
        self._todo_path = todo_path or os.path.join(os.getcwd(), "todo.md")
        self._todos = []

    @staticmethod
    def get_tool_name():
        return "todo_write"

    async def act(
        self,
        action: Literal["add", "complete", "list", "clear"],
        content: Optional[str] = None,
        todo_id: Optional[int] = None
    ):
        self._load_todos()
        
        if action == "add":
            if not content:
                return {"error": "Content is required for adding a todo"}
            return self._add_todo(content)
        
        elif action == "complete":
            if todo_id is None:
                return {"error": "todo_id is required for completing a todo"}
            return self._complete_todo(todo_id)
        
        elif action == "list":
            return self._list_todos()
        
        elif action == "clear":
            return self._clear_completed()
        
        else:
            return {"error": f"Unknown action: {action}"}

    def _add_todo(self, content: str) -> dict:
        todo_id = len(self._todos)
        self._todos.append({
            "id": todo_id,
            "content": content,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        })
        self._save_todos()
        return {"result": f"Added todo #{todo_id}", "id": todo_id}

    def _complete_todo(self, todo_id: int) -> dict:
        for todo in self._todos:
            if todo["id"] == todo_id:
                todo["status"] = "completed"
                todo["completed_at"] = datetime.now().isoformat()
                self._save_todos()
                return {"result": f"Completed todo #{todo_id}"}
        return {"error": f"Todo #{todo_id} not found"}

    def _list_todos(self) -> dict:
        pending = [t for t in self._todos if t["status"] == "pending"]
        completed = [t for t in self._todos if t["status"] == "completed"]
        return {
            "result": f"{len(pending)} pending, {len(completed)} completed",
            "pending": pending,
            "completed": completed
        }

    def _clear_completed(self) -> dict:
        original_count = len(self._todos)
        self._todos = [t for t in self._todos if t["status"] != "completed"]
        cleared = original_count - len(self._todos)
        self._save_todos()
        return {"result": f"Cleared {cleared} completed todos"}

    def _load_todos(self):
        path = Path(self._todo_path)
        self._todos = []
        
        if not path.exists():
            return
        
        try:
            content = path.read_text(encoding="utf-8")
            todo_id = 0
            for line in content.strip().split("\n"):
                if line.startswith("- [x] "):
                    self._todos.append({
                        "id": todo_id,
                        "content": line[6:],
                        "status": "completed"
                    })
                    todo_id += 1
                elif line.startswith("- [ ] "):
                    self._todos.append({
                        "id": todo_id,
                        "content": line[6:],
                        "status": "pending"
                    })
                    todo_id += 1
        except IOError:
            pass

    def _save_todos(self):
        lines = ["# Todo List", ""]
        
        pending = [t for t in self._todos if t["status"] == "pending"]
        completed = [t for t in self._todos if t["status"] == "completed"]
        
        if pending:
            lines.append("## Pending")
            for todo in pending:
                lines.append(f"- [ ] {todo['content']}")
            lines.append("")
        
        if completed:
            lines.append("## Completed")
            for todo in completed:
                lines.append(f"- [x] {todo['content']}")
            lines.append("")
        
        content = "\n".join(lines)
        Path(self._todo_path).write_text(content, encoding="utf-8")

    def json_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.get_tool_name(),
                "description": TOOL_DESCRIPTION,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["add", "complete", "list", "clear"],
                            "description": "The action to perform."
                        },
                        "content": {
                            "type": "string",
                            "description": "The todo content (required for 'add' action)."
                        },
                        "todo_id": {
                            "type": "integer",
                            "description": "The todo ID (required for 'complete' action)."
                        }
                    },
                    "required": ["action"]
                }
            }
        }
