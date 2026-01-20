import os
from typing import Dict, Any, List, Optional, TYPE_CHECKING, Protocol

from src.tools.base import BaseTool

if TYPE_CHECKING:
    from src.history.manager import HistoryManager
    from src.subagents.manager import SubagentManager


class UIProtocol(Protocol):
    def print_info(self, message: str) -> None: ...


TOOL_REGISTRY = {
    # Execution
    "cmd_runner": ("src.tools.execution.terminal", "CmdRunner"),
    
    # Filesystem
    "read_file": ("src.tools.filesystem.read", "ReadFileTool"),
    "edit_file": ("src.tools.filesystem.edit", "EditFileTool"),
    "search_replace": ("src.tools.filesystem.search_replace", "SearchReplaceTool"),
    "delete_file": ("src.tools.filesystem.delete", "DeleteFileTool"),
    "list_dir": ("src.tools.filesystem.list_dir", "ListDirTool"),
    
    # Search (explorer only)
    "grep_search": ("src.tools.search.grep", "GrepSearchTool"),
    "file_search": ("src.tools.search.file_search", "FileSearchTool"),
    "ripgrep": ("src.tools.search.ripgrep", "RipgrepTool"),
    "glob": ("src.tools.search.glob", "GlobTool"),
    
    # Code Analysis (explorer only)
    "extract_symbols": ("src.tools.code.symbols", "ExtractSymbolsTool"),
    "get_context": ("src.tools.code.context", "GetContextTool"),
    "repo_structure": ("src.tools.code.structure", "RepoStructureTool"),
    
    # Git
    "git_status": ("src.tools.git.status", "GitStatusTool"),
    "git_diff": ("src.tools.git.diff", "GitDiffTool"),
    "git_commit": ("src.tools.git.commit", "GitCommitTool"),
    
    # Memory
    "add_memory": ("src.tools.memory.add", "AddMemoryTool"),
    "list_memories": ("src.tools.memory.list", "ListMemoriesTool"),
    
    # Utilities
    "context_compression": ("src.tools.utilities.compression", "ContextCompressionTool"),
    "todo_write": ("src.tools.utilities.todo", "TodoTool"),
    "task": ("src.tools.utilities.task", "TaskTool"),
    "scratchpad": ("src.tools.utilities.scratchpad", "ScratchpadTool"),
    
    # Delegation
    "delegate": ("src.tools.delegate", "DelegateTool"),
}

# Tools that ONLY the explorer sub-agent should use
# Main agent should delegate to explorer for deep code analysis
EXPLORER_ONLY_TOOLS = {
    "extract_symbols",
    "get_context",
    "repo_structure",
}


class ToolManager:
    
    def __init__(
        self, 
        history_manager: Optional["HistoryManager"] = None, 
        ui_manager: Optional[UIProtocol] = None, 
        subagent_manager: Optional["SubagentManager"] = None,
        workspace_root: Optional[str] = None
    ):
        self.tools: Dict[str, BaseTool] = {}
        self._tool_classes: Dict[str, type] = {}
        self.history_manager = history_manager
        self.ui_manager = ui_manager
        self.subagent_manager = subagent_manager
        self.workspace_root = workspace_root or os.getcwd()
        self._tools_initialized = False

    def _ensure_tools_loaded(self):
        if self._tools_initialized:
            return
        self._tools_initialized = True
        
        for name, (module_path, class_name) in TOOL_REGISTRY.items():
            if name == "context_compression" and not self.history_manager:
                continue
            if name == "todo_write" and not self.ui_manager:
                continue
            if name == "task" and not (self.subagent_manager and self.ui_manager):
                continue
            
            try:
                import importlib
                module = importlib.import_module(module_path)
                tool_class = getattr(module, class_name)
                
                if name == "context_compression":
                    self.tools[name] = tool_class(history_manager=self.history_manager)
                elif name == "todo_write":
                    self.tools[name] = tool_class(ui_manager=self.ui_manager)
                elif name == "task":
                    self.tools[name] = tool_class(
                        subagent_manager=self.subagent_manager,
                        ui_manager=self.ui_manager
                    )
                elif name == "scratchpad":
                    self.tools[name] = tool_class(ui_manager=self.ui_manager)
                # Search and code analysis tools get workspace_root
                elif name in ("ripgrep", "glob", "grep_search", "file_search", "extract_symbols"):
                    self.tools[name] = tool_class(workspace_root=self.workspace_root)
                else:
                    self.tools[name] = tool_class()
            except Exception:
                pass

    def register_tool(self, tool: BaseTool):
        self.tools[tool.get_tool_name()] = tool

    def get_tool(self, name: str) -> Optional[BaseTool]:
        self._ensure_tools_loaded()
        return self.tools.get(name)

    def get_tools_description(self) -> List[Dict[str, Any]]:
        self._ensure_tools_loaded()
        return [tool.json_schema() for tool in self.tools.values()]
    
    def get_main_agent_tools(self) -> List[Dict[str, Any]]:
        """Get tools for the main agent (excludes explorer-only tools)."""
        self._ensure_tools_loaded()
        return [
            tool.json_schema() 
            for name, tool in self.tools.items() 
            if name not in EXPLORER_ONLY_TOOLS
        ]

    def get_tool_status(self, tool_name: str) -> str:
        tool = self.get_tool(tool_name)
        if not tool:
            return f"Tool '{tool_name}' not found."
        if hasattr(tool, 'get_status'):
            return tool.get_status()
        return f"Tool '{tool_name}' does not have a status."

    async def run_tool(self, tool_name: str, **kwargs) -> Any:
        tool = self.get_tool(tool_name)
        if not tool:
            return f"Error: Tool '{tool_name}' not found."
        
        return await tool.act(**kwargs)
