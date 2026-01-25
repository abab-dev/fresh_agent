from typing import Literal, Optional, Protocol, List, Dict
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Manage a todo list for tracking task progress.

## When to Use This Tool
Use proactively for:
1. Complex multi-step tasks (3+ distinct steps)
2. User provides multiple tasks (numbered or comma-separated list)
3. Feature implementation requiring multiple files
4. Non-trivial work: investigate → implement → verify

## When NOT to Use This Tool
Skip when:
1. Single straightforward task
2. Trivial task (less than 3 steps)
3. Purely informational/conversational requests
4. You can complete the work in 1-2 tool calls

RULE: If you can finish in 1-2 tool calls, just do it directly.

## Actions
- add: Add new todo item(s)
- start: Mark a todo as in_progress (BEFORE you begin work)
- complete: Mark a todo as completed (IMMEDIATELY after finishing)
- list: Show all todos
- clear: Remove completed todos

## Workflow
1. Add all tasks upfront when you understand the scope
2. Mark exactly ONE task as in_progress at a time
3. Complete tasks IMMEDIATELY after finishing (don't batch)
4. Only mark complete when FULLY done (not partial)

## Example
User: "Add user registration with validation"

todo_write(action="add", content="Create user model")
todo_write(action="add", content="Add validation logic")
todo_write(action="add", content="Create registration endpoint")
todo_write(action="add", content="Add tests")
todo_write(action="start", todo_id=0)
# ... work on first task ...
todo_write(action="complete", todo_id=0)
todo_write(action="start", todo_id=1)
# ... continue ..."""


class UIProtocol(Protocol):
    def print_info(self, message: str) -> None: ...
    def emit(self, msg_type: str, data: dict) -> None: ...


class TodoTool(BaseTool):
    def __init__(self, ui_manager: Optional[UIProtocol] = None):
        super().__init__()
        self._ui_manager = ui_manager
        self._todos: List[Dict] = []
        self._next_id = 0

    @staticmethod
    def get_tool_name():
        return "todo_write"

    def _emit_update(self):
        """Emit todo list update to UI."""
        if self._ui_manager and hasattr(self._ui_manager, 'emit'):
            self._ui_manager.emit("todo_update", {"todos": self._todos})

    def _get_summary(self) -> str:
        """Get a one-line summary of todo status."""
        pending = sum(1 for t in self._todos if t["status"] == "pending")
        in_progress = sum(1 for t in self._todos if t["status"] == "in_progress")
        completed = sum(1 for t in self._todos if t["status"] == "completed")
        total = len(self._todos)
        return f"{completed}/{total} complete, {in_progress} in progress, {pending} pending"

    async def act(
        self,
        action: Literal["add", "start", "complete", "list", "clear"],
        content: Optional[str] = None,
        todo_id: Optional[int] = None
    ):
        if action == "add":
            if not content:
                return {"error": "Content is required for adding a todo"}
            return self._add_todo(content)
        
        elif action == "start":
            if todo_id is None:
                return {"error": "todo_id is required for starting a todo"}
            return self._start_todo(todo_id)
        
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
        todo_id = self._next_id
        self._next_id += 1
        
        self._todos.append({
            "id": todo_id,
            "content": content,
            "status": "pending"
        })
        
        self._emit_update()
        return {
            "result": f"Added todo #{todo_id}: {content}",
            "id": todo_id,
            "summary": self._get_summary()
        }

    def _start_todo(self, todo_id: int) -> dict:
        # Check if another task is already in progress
        in_progress = [t for t in self._todos if t["status"] == "in_progress"]
        if in_progress:
            return {
                "error": f"Task #{in_progress[0]['id']} is already in progress. Complete it first.",
                "hint": "Only ONE task should be in_progress at a time."
            }
        
        for todo in self._todos:
            if todo["id"] == todo_id:
                if todo["status"] == "completed":
                    return {"error": f"Todo #{todo_id} is already completed"}
                
                todo["status"] = "in_progress"
                self._emit_update()
                return {
                    "result": f"Started: {todo['content']}",
                    "summary": self._get_summary()
                }
        
        return {"error": f"Todo #{todo_id} not found"}

    def _complete_todo(self, todo_id: int) -> dict:
        for todo in self._todos:
            if todo["id"] == todo_id:
                if todo["status"] == "completed":
                    return {"error": f"Todo #{todo_id} is already completed"}
                
                todo["status"] = "completed"
                self._emit_update()
                
                # Find next pending task
                next_pending = next(
                    (t for t in self._todos if t["status"] == "pending"),
                    None
                )
                hint = ""
                if next_pending:
                    hint = f" Next: #{next_pending['id']} - {next_pending['content']}"
                
                return {
                    "result": f"Completed: {todo['content']}.{hint}",
                    "summary": self._get_summary()
                }
        
        return {"error": f"Todo #{todo_id} not found"}

    def _list_todos(self) -> dict:
        if not self._todos:
            return {"result": "No todos", "todos": []}
        
        lines = []
        for todo in self._todos:
            status_icon = {
                "pending": "○",
                "in_progress": "▶",
                "completed": "✓"
            }.get(todo["status"], "?")
            lines.append(f"{status_icon} #{todo['id']}: {todo['content']}")
        
        return {
            "result": "\n".join(lines),
            "todos": self._todos,
            "summary": self._get_summary()
        }

    def _clear_completed(self) -> dict:
        original_count = len(self._todos)
        self._todos = [t for t in self._todos if t["status"] != "completed"]
        cleared = original_count - len(self._todos)
        
        self._emit_update()
        return {
            "result": f"Cleared {cleared} completed todos",
            "summary": self._get_summary()
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
                        "action": {
                            "type": "string",
                            "enum": ["add", "start", "complete", "list", "clear"],
                            "description": "The action to perform."
                        },
                        "content": {
                            "type": "string",
                            "description": "The todo content (required for 'add' action)."
                        },
                        "todo_id": {
                            "type": "integer",
                            "description": "The todo ID (required for 'start' and 'complete' actions)."
                        }
                    },
                    "required": ["action"]
                }
            }
        }
