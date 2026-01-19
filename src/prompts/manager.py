import os
from abc import ABC, abstractmethod
from pathlib import Path

from src.prompts.environment import get_environment_info
from src.prompts.system import get_system_rules
from src.prompts.reminders import get_reminders as _get_reminders


AGENT_INSTRUCTIONS_FILE = "AGENT.md"


def load_project_instructions() -> str:
    instructions_path = Path(os.getcwd()) / AGENT_INSTRUCTIONS_FILE
    if not instructions_path.exists():
        return ""
    
    try:
        content = instructions_path.read_text().strip()
        return f"\n\n## Project Instructions (from {AGENT_INSTRUCTIONS_FILE})\n{content}" if content else ""
    except IOError:
        return ""


class BasePromptManager(ABC):
    @abstractmethod
    def get_system_prompt(self) -> str:
        pass


class PromptManager(BasePromptManager):
    def __init__(self):
        pass

    def get_system_prompt(self) -> str:
        return f"""
{get_system_rules()}

{get_environment_info()}
{load_project_instructions()}
""".strip()

    def get_reminders(self, tool_manager=None) -> str:
        return _get_reminders(tool_manager)
