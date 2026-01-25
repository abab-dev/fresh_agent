#!/usr/bin/env python3
"""
Bridge UI - Emits JSON messages for the terminal UI frontend.
Implements the same interface as SimpleUI but communicates via stdio.
"""
import asyncio
import json
import sys
import os
from typing import Tuple


class BridgeUI:
    """UI that communicates with the Ink frontend via JSON over stdio."""
    
    def __init__(self):
        self._streaming = False
        self._stream_buffer = ""
    
    def emit(self, msg_type: str, data: dict) -> None:
        """Send a message to the frontend."""
        msg = json.dumps({"type": msg_type, "data": data})
        print(f"__MSG__{msg}__END__", flush=True)
    
    def print_simple_message(self, message: str, prefix: str = "") -> None:
        self.emit("message", {"content": message, "prefix": prefix})
    
    def print_info(self, message: str) -> None:
        self.emit("info", {"content": message})
    
    def print_assistant_message(self, message: str) -> None:
        self.emit("assistant_message", {"content": message})
    
    async def get_user_input(self) -> str:
        """Read user input from stdin (JSON format)."""
        loop = asyncio.get_event_loop()
        try:
            line = await loop.run_in_executor(None, sys.stdin.readline)
            if not line:
                return "/exit"
            msg = json.loads(line.strip())
            if msg.get("type") == "user_input":
                return msg.get("data", {}).get("message", "")
            elif msg.get("type") == "stop_agent":
                return "/stop"
            return ""
        except (json.JSONDecodeError, EOFError):
            return "/exit"
    
    def start_stream_display(self) -> None:
        self._streaming = True
        self._stream_buffer = ""
        self.emit("stream_start", {})
    
    def print_streaming_content(self, content: str) -> None:
        self._stream_buffer += content
        self.emit("stream_chunk", {"content": content})
    
    def stop_stream_display(self) -> None:
        self._streaming = False
        self.emit("stream_end", {"content": self._stream_buffer})
        self._stream_buffer = ""
    
    def show_preparing_tool(self, name: str, args: dict) -> None:
        self.emit("tool_preparing", {"name": name, "args": args})
    
    def show_tool_execution(self, name: str, args: dict, success: bool, result: str) -> None:
        self.emit("tool_result", {
            "name": name,
            "args": args,
            "success": success,
            "result": result
        })
    
    async def wait_for_user_approval(self, content: str) -> Tuple[bool, str]:
        """Request tool approval from the frontend."""
        # Parse tool name and args from content
        tool_name = "tool_execution"
        args = content
        
        if "Tool:" in content:
            parts = content.split(",", 1)
            if parts:
                tool_name = parts[0].replace("Tool:", "").strip()
                args = parts[1].strip() if len(parts) > 1 else ""
        
        self.emit("tool_request", {"name": tool_name, "args": args})
        
        # Wait for approval response
        loop = asyncio.get_event_loop()
        try:
            line = await loop.run_in_executor(None, sys.stdin.readline)
            if not line:
                return False, "Connection closed"
            msg = json.loads(line.strip())
            if msg.get("type") == "tool_approval":
                approved = msg.get("data", {}).get("approved", False)
                response = msg.get("data", {}).get("content", "")
                return approved, response
            return False, "Invalid response"
        except (json.JSONDecodeError, EOFError):
            return False, "Error reading approval"
    
    def set_status(self, status: str) -> None:
        """Update status line."""
        self.emit("turn_status", {"state": status})
    
    def set_thinking(self) -> None:
        self.emit("thinking", {})
    
    def set_executing(self, tool_name: str) -> None:
        self.emit("tool_executing", {"name": tool_name})
    
    def todo_update(self, todos: list) -> None:
        """Emit updated todo list to frontend."""
        self.emit("todo_update", {"todos": todos})
    
    # Subagent events
    def subagent_start(self, agent_name: str, task: str) -> None:
        """Called when a subagent is spawned."""
        self.emit("subagent_start", {"agent": agent_name, "task": task})
    
    def subagent_tool(self, agent_name: str, tool_name: str, args: dict) -> None:
        """Called when a subagent executes a tool."""
        self.emit("subagent_tool", {
            "agent": agent_name,
            "name": tool_name,
            "args": args
        })
    
    def subagent_tool_result(self, agent_name: str, tool_name: str, success: bool, result: str) -> None:
        """Called when a subagent tool completes."""
        self.emit("subagent_tool_result", {
            "agent": agent_name,
            "name": tool_name,
            "success": success,
            "result": result[:500]  # Truncate for display
        })
    
    def subagent_complete(self, agent_name: str, result: str) -> None:
        """Called when a subagent completes its task."""
        self.emit("subagent_complete", {
            "agent": agent_name,
            "result": result[:1000]  # Truncate for display
        })


async def main():
    """Main entry point for the bridge."""
    import argparse
    from src.agent.factory import AgentFactory
    
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="Run the coding agent (bridge mode)")
    parser.add_argument(
        "--repo-path", "-r",
        type=str,
        default=None,
        help="Path to the repository to work in (also: REPO_PATH env var)"
    )
    args = parser.parse_args()
    
    # Determine working directory: CLI flag > env var > current dir
    repo_path = args.repo_path or os.environ.get("REPO_PATH", None)
    
    if repo_path:
        repo_path = os.path.abspath(os.path.expanduser(repo_path))
        if os.path.isdir(repo_path):
            os.chdir(repo_path)
        else:
            print(f"Error: Directory not found: {repo_path}", file=sys.stderr)
            sys.exit(1)
    
    ui = BridgeUI()
    
    # Send ready signal
    ui.emit("ready", {})
    
    # Send environment info
    ui.emit("environment_info", {
        "working_directory": os.getcwd()
    })
    
    try:
        # Determine workspace - use repo_path if set, otherwise cwd
        workspace = repo_path or os.getcwd()
        agent = AgentFactory.create_agent(ui_manager=ui, workspace_root=workspace)
        await agent.start_conversation()
    except KeyboardInterrupt:
        ui.emit("stopped", {"reason": "User interrupted"})
    except Exception as e:
        ui.emit("error", {"message": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

