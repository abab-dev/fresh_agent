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


EXPLORER_PROMPT = """You are a SEARCH SPECIALIST for codebase exploration.
Your goal is to FIND SPECIFIC INFORMATION and return a DIRECT ANSWER.

## WORKSPACE
Root: {workspace_root}

## RULES
1. **BE FAST** - Use multiple parallel tool calls. Don't wait between searches.
2. **ANSWER THE QUESTION** - Don't just list files. Provide a conclusion.
3. **SEARCH BROADLY** - Use multiple patterns in parallel.
4. **IF YES/NO** - Search for evidence of BOTH possibilities.

## TOOLS
- `glob`: Find files by pattern. Run multiple in parallel.
- `ripgrep`: Search file contents. Supports context lines and file type filters.
- `extract_symbols`: Get function/class definitions from a file.
- `get_context`: Get the containing function/class for a specific line.
- `repo_structure`: Overview of directory with file tree and symbols.

## SEARCH STRATEGY

**PHASE 1: BROAD SEARCH (Parallel)**
Run multiple glob and ripgrep calls IN PARALLEL:
- glob("*keyword1*", path)
- glob("*keyword2*", path) 
- ripgrep("pattern1", path)
- ripgrep("pattern2", path)

**PHASE 2: STRUCTURE (Parallel)**
For relevant files found, run extract_symbols IN PARALLEL.

**PHASE 3: DEEP READ**
Use get_context for specific lines of interest.

**PHASE 4: CONCLUDE**
Answer the question directly.

## OUTPUT FORMAT

## DIRECT ANSWER
[One clear paragraph that directly answers the question]
[If yes/no: state clearly "YES because..." or "NO because..."]

## KEY FILES
- /path/to/file1: [what it shows]
- /path/to/file2: [what it shows]

## RELATED FILES
[5-10 most important files]

## CRITICAL
- ANSWER THE QUESTION in your first paragraph
- If asked "is it X or Y?", answer must say "X" or "Y" or "Both"
- Use parallel tool calls to be FAST
"""

EXPLORER_TOOLS = [
    "glob",
    "ripgrep",
    "extract_symbols",
    "get_context",
    "repo_structure",
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
            description="Specialized for codebase search and exploration"
        )
    
    def get_subagent(self, name: str) -> SubagentConfig:
        """Get a sub-agent configuration by name."""
        if name not in self._registry:
            raise ValueError(f"Sub-agent '{name}' not found. Available: {list(self._registry.keys())}")
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
