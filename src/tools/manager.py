import os
import importlib
from typing import Dict, Optional

from src.tools.base import BaseTool


TOOL_REGISTRY = {
    "cmd_runner": ("src.tools.execution.terminal", "CmdRunner"),
    "read_file": ("src.tools.filesystem.read", "ReadFileTool"),
    "edit_file": ("src.tools.filesystem.edit", "EditFileTool"),
    "search_replace": ("src.tools.filesystem.search_replace", "SearchReplaceTool"),
    "delete_file": ("src.tools.filesystem.delete", "DeleteFileTool"),
    "list_dir": ("src.tools.filesystem.list_dir", "ListDirTool"),
    "grep_search": ("src.tools.search.grep", "GrepSearchTool"),
    "file_search": ("src.tools.search.file_search", "FileSearchTool"),
    "ripgrep": ("src.tools.search.ripgrep", "RipgrepTool"),
    "glob": ("src.tools.search.glob", "GlobTool"),
    "extract_symbols": ("src.tools.code.symbols", "ExtractSymbolsTool"),
    "get_context": ("src.tools.code.context", "GetContextTool"),
    "repo_structure": ("src.tools.code.structure", "RepoStructureTool"),
    "git_status": ("src.tools.git.status", "GitStatusTool"),
    "git_diff": ("src.tools.git.diff", "GitDiffTool"),
    "git_commit": ("src.tools.git.commit", "GitCommitTool"),
    "add_memory": ("src.tools.memory.add", "AddMemoryTool"),
    "list_memories": ("src.tools.memory.list", "ListMemoriesTool"),
    "scratchpad": ("src.tools.utilities.scratchpad", "ScratchpadTool"),
}


class ToolManager:
    def __init__(self, workspace_root: Optional[str] = None):
        self.tools: Dict[str, BaseTool] = {}
        self.workspace_root = workspace_root or os.getcwd()
        self._tools_initialized = False

    def _ensure_tools_loaded(self):
        if self._tools_initialized:
            return
        self._tools_initialized = True

        for name, (module_path, class_name) in TOOL_REGISTRY.items():
            try:
                module = importlib.import_module(module_path)
                tool_class = getattr(module, class_name)

                if name in ("ripgrep", "glob", "grep_search", "file_search", "extract_symbols"):
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

    def get_tools_description(self):
        self._ensure_tools_loaded()
        return [tool.json_schema() for tool in self.tools.values()]
