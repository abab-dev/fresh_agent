from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.tools.manager import ToolManager


def get_reminders(tool_manager: "ToolManager" = None) -> str:
    reminders = []
    
    reminders.append("Remember: Use absolute paths for all file operations.")
    reminders.append("Remember: Set need_user_approve=true for destructive commands.")
    
    if tool_manager:
        todo_tool = tool_manager.get_tool("todo_write")
        if todo_tool:
            try:
                pending = [t for t in getattr(todo_tool, '_todos', []) if t.get('status') == 'pending']
                if pending:
                    reminders.append(f"You have {len(pending)} pending todos. Complete them before finishing.")
            except:
                pass
    
    if not reminders:
        return ""
    
    return "\n[REMINDERS]\n" + "\n".join(f"- {r}" for r in reminders)
