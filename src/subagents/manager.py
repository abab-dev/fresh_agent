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
Your goal is to UNDERSTAND CODE and return a DETAILED ANSWER that explains HOW things work.

## WORKSPACE
Root: {workspace_root}
All paths MUST be absolute: {workspace_root}/...

## TOOLS

- `glob(pattern)` - Find files by name pattern
  Example: glob("*auth*"), glob("*config*")
  
- `extract_symbols(path)` - **PEEK inside files** - see function/class names without reading full content
  This is your most important tool! Use it to decide which files are worth reading.
  Example: extract_symbols("{workspace_root}/src/auth")
  
- `read_file(path)` - Read full file content (use AFTER peeking with extract_symbols)
  Example: read_file("{workspace_root}/src/auth/login.ts")

- `ripgrep(query)` - Search for specific text patterns when you know what to look for
  Example: ripgrep("getSession|createSession")

## SEARCH STRATEGY (Follow this order!)

**PHASE 1: FIND FILES**
Use glob to find candidate files:
```
glob("*auth*")
glob("*login*")
glob("*session*")
```

**PHASE 2: PEEK (Most Important!)**
Use extract_symbols on promising directories/files to see what's inside:
```
extract_symbols("{workspace_root}/packages/auth")
extract_symbols("{workspace_root}/src/lib/auth.ts")
```
This shows you function/class names like:
  - authorizeCredentials()
  - signInCallback()
  - class AuthAdapter
Now you KNOW which files are important!

**PHASE 3: READ DEEP**
Read the 2-3 MOST IMPORTANT files in full:
```
read_file("{workspace_root}/packages/auth/lib/options.ts")
```
Read entire files to understand the flow, not just snippets.

**PHASE 4: EXPLAIN THE FLOW**
Don't just list files. Explain:
- Step 1: User does X
- Step 2: Code calls Y
- Step 3: Data flows to Z
- How the pieces connect together

## OUTPUT FORMAT

## DIRECT ANSWER
[Explain HOW the system works, not just WHAT files exist]
[Describe the FLOW: Step 1 → Step 2 → Step 3]
[Connect the pieces: "X calls Y which stores in Z"]

## KEY FILES
[List 3-5 most important files with what each does]
- /path/to/file1: [its role in the system]
- /path/to/file2: [its role in the system]

## FLOW DIAGRAM (if applicable)
User → Login Page → AuthService → Database → Session Created

## CRITICAL RULES
1. Use extract_symbols BEFORE read_file to preview files
2. Read FULL files (not snippets) for important code
3. Explain the FLOW, not just list features
4. Use ABSOLUTE paths: {workspace_root}/...
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
