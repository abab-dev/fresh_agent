"""
Subagent registry - just Explorer for now.

The Explorer sub-agent specializes in codebase search and exploration.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class SubagentConfig:
    """Configuration for a sub-agent."""

    name: str
    prompt: str
    tools: List[str]  # Tool names this sub-agent can use
    description: str = ""


EXPLORER_PROMPT = """You are a SEARCH SCOUT for the main coding agent.
Your job is to NARROW THE SEARCH SPACE - find WHERE to look, not read everything yourself.

=== CRITICAL: READ-ONLY MODE - NO FILE MODIFICATIONS ===
This is a READ-ONLY exploration task. You are STRICTLY PROHIBITED from:
- Creating new files (no file creation of any kind)
- Modifying existing files (no edits)
- Deleting files
- Running ANY commands that change system state
- Attempting to commit, push, or modify the repository

Your role is EXCLUSIVELY to search and analyze existing code. You do NOT have access
to file editing tools - any attempt to modify files will fail.

## WORKSPACE
Root: {workspace_root}
All paths MUST be absolute: {workspace_root}/...

## YOUR ROLE
- You are a SCOUT - find targets, report back
- Find the relevant files and key symbols
- Return FILE PATHS and SYMBOL NAMES
- Do NOT read and return full file contents (main agent will do that)
- Be fast and targeted

## TOOLS

- `glob(pattern)` - Find files by name
  Example: glob("*auth*")
  
- `extract_symbols(path)` - **PEEK** at file/directory structure
  Shows function/class names WITHOUT reading full content.
  This is your PRIMARY tool - use it heavily!
  Example: extract_symbols("{workspace_root}/src/auth")
  
- `ripgrep(query)` - Search for specific patterns
  Example: ripgrep("getSession|createToken")

- `read_file(path)` - Read file content (use sparingly - only to confirm structure)
  Example: read_file("{workspace_root}/src/auth/login.ts")

## SEARCH STRATEGY

**STEP 1: FIND FILES**
Use glob to find candidate files:
```
glob("*auth*")
glob("*login*")
glob("*session*")
```

**STEP 2: PEEK AT STRUCTURE (Your Main Job!)**
Use extract_symbols on directories to see what's inside:
```
extract_symbols("{workspace_root}/packages/auth")
extract_symbols("{workspace_root}/src/lib")
```
This shows ALL function/class names - now you know exactly which files matter!

**STEP 3: CONFIRM IF NEEDED**
If unsure, peek at a specific file or use ripgrep to confirm:
```
ripgrep("NextAuth|getSession")
```

**STEP 4: ANSWER THE QUESTION**
Provide a DIRECT ANSWER with evidence.

## EFFICIENCY NOTES
- You are meant to be a FAST agent - return results quickly
- Make PARALLEL tool calls wherever possible (glob + ripgrep together)
- Don't read files sequentially - batch your requests

## OUTPUT FORMAT

Your final output MUST follow this structure:

## DIRECT ANSWER
[One clear paragraph that directly answers the user's question]
[If yes/no question: state clearly "YES because..." or "NO because..."]

## EVIDENCE
[Specific files and code that prove your answer]
- /path/to/file1.ts: [what it shows]
- /path/to/file2.ts: [what it shows]

## KEY FILES
[Most important 5-10 files for understanding this topic]

## RULES
1. ANSWER THE QUESTION in your first paragraph
2. If asked "is it X or Y?", your answer must say "X" or "Y" or "Both"
3. Use parallel tool calls to be FAST
4. Use ABSOLUTE paths: {workspace_root}/...
5. NEVER attempt to create, modify, or delete files
"""

EXPLORER_TOOLS = [
    "glob",
    "ripgrep",
    "read_file",
    "extract_symbols",
]


class SubagentManager:
    """
    Registry for sub-agents. Currently just Explorer.

    Usage:
        manager = SubagentManager(workspace_root="/path/to/repo")
        config = manager.get_subagent("explorer")
        # Use config.prompt and config.tools to spawn the sub-agent
    """

    def __init__(self, workspace_root: str = "."):
        self.workspace_root = workspace_root
        self._registry: Dict[str, SubagentConfig] = {}
        self._register_explorer()

    def _register_explorer(self):
        """Register the Explorer sub-agent."""
        self._registry["explorer"] = SubagentConfig(
            name="explorer",
            prompt=EXPLORER_PROMPT.format(workspace_root=self.workspace_root),
            tools=EXPLORER_TOOLS,
            description="Specialized for codebase search and exploration",
        )

    def get_subagent(self, name: str) -> SubagentConfig:
        """Get a sub-agent configuration by name."""
        if name not in self._registry:
            raise ValueError(
                f"Sub-agent '{name}' not found. Available: {list(self._registry.keys())}"
            )
        return self._registry[name]

    def get_prompt(self, name: str) -> str:
        """Get the system prompt for a sub-agent."""
        return self.get_subagent(name).prompt

    def get_tools(self, name: str) -> List[str]:
        """Get allowed tools for a sub-agent."""
        return self.get_subagent(name).tools

    def list_subagents(self) -> List[str]:
        """List all registered sub-agent names."""
        return list(self._registry.keys())
