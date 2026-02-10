import asyncio
import os
import shutil
from typing import Optional
from src.tools.base import BaseTool


TOOL_DESCRIPTION = """Search for text in files using ripgrep.

Fast text search across the codebase. Uses ripgrep when available, falls back to grep.

Args:
    query: Text or regex pattern to search for
    path: Directory or file to search (default: workspace root)
    context_lines: Lines of context before/after matches (default: 2)

Use cases:
- Find function/class definitions
- Locate error messages or strings
- Track down variable usage
- Search for TODO/FIXME comments"""


class RipgrepTool(BaseTool):
    def __init__(self, workspace_root: str = None):
        super().__init__()
        self._has_ripgrep = shutil.which("rg") is not None
        self._workspace_root = workspace_root or os.getcwd()

    @staticmethod
    def get_tool_name():
        return "ripgrep"

    def _resolve_path(self, path: Optional[str]) -> str:
        """Resolve path to absolute. Default to workspace root."""
        if path is None:
            return self._workspace_root

        # If relative, make absolute from workspace root
        if not os.path.isabs(path):
            return os.path.join(self._workspace_root, path)

        return path

    async def act(self, query: str, path: Optional[str] = None, context_lines: int = 2):
        """
        Search for pattern in files.

        Args:
            query: Text pattern to search for (supports regex with | for OR)
            path: Directory or file to search (default: workspace root)
            context_lines: Lines of context around matches (default: 2)
        """
        search_path = self._resolve_path(path)

        if not os.path.exists(search_path):
            return {"error": f"Path not found: {search_path}"}

        if self._has_ripgrep:
            return await self._search_ripgrep(query, search_path, context_lines)
        else:
            return await self._search_grep(query, search_path, context_lines)

    async def _search_ripgrep(self, query: str, path: str, context_lines: int):
        cmd = [
            "rg",
            "--json",
            "--no-heading",
            "-C",
            str(context_lines),
            "--max-count",
            "100",
        ]
        cmd.extend(["--", query, path])

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            stdout, _ = await asyncio.wait_for(process.communicate(), timeout=60)
            output = stdout.decode("utf-8", errors="replace")
            matches = self._parse_ripgrep_json(output)

            return {
                "result": f"Found {len(matches)} matches",
                "matches": matches,
                "truncated": len(matches) >= 100,
                "engine": "ripgrep",
            }

        except asyncio.TimeoutError:
            return {"error": "Search timed out after 60s"}
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

    def _parse_ripgrep_json(self, output: str) -> list:
        import json

        matches = []

        for line in output.strip().split("\n"):
            if not line:
                continue
            try:
                msg = json.loads(line)
                if msg.get("type") == "match":
                    data = msg.get("data", {})
                    file_path = data.get("path", {}).get("text", "")
                    line_num = data.get("line_number", 0)
                    lines_data = data.get("lines", {})
                    content = lines_data.get("text", "").strip()

                    matches.append(
                        {"file": file_path, "line": line_num, "content": content[:500]}
                    )

                    if len(matches) >= 100:
                        break
            except json.JSONDecodeError:
                continue

        return matches

    async def _search_grep(self, query: str, path: str, context_lines: int):
        cmd = ["grep", "-rn", "--color=never", f"-C{context_lines}"]

        # Default excludes
        for exc in [
            ".git",
            "node_modules",
            "__pycache__",
            ".venv",
            "venv",
            "dist",
            "build",
        ]:
            cmd.extend(["--exclude-dir", exc])

        cmd.extend(["--", query, path])

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            stdout, _ = await asyncio.wait_for(process.communicate(), timeout=60)
            output = stdout.decode("utf-8", errors="replace")
            matches = []

            for line in output.strip().split("\n")[:100]:
                if ":" in line:
                    parts = line.split(":", 2)
                    if len(parts) >= 3:
                        matches.append(
                            {
                                "file": parts[0],
                                "line": int(parts[1]) if parts[1].isdigit() else 0,
                                "content": parts[2].strip()[:500],
                            }
                        )

            return {
                "result": f"Found {len(matches)} matches",
                "matches": matches,
                "truncated": len(matches) >= 100,
                "engine": "grep",
            }

        except asyncio.TimeoutError:
            return {"error": "Search timed out"}
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

    def json_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.get_tool_name(),
                "description": TOOL_DESCRIPTION,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Text pattern to search for. Supports regex (use | for OR patterns).",
                        },
                        "path": {
                            "type": "string",
                            "description": "Directory or file to search. Default: workspace root.",
                        },
                        "context_lines": {
                            "type": "integer",
                            "description": "Lines of context around matches. Default: 2.",
                            "default": 2,
                        },
                    },
                    "required": ["query"],
                },
            },
        }
