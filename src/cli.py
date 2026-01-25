#!/usr/bin/env python3
"""
Simple CLI entry point for the agent.
"""
from dotenv import load_dotenv
load_dotenv()

import asyncio
import sys
from typing import Tuple


class SimpleUI:
    """Minimal console UI for the agent."""
    
    def print_simple_message(self, message: str, prefix: str = "") -> None:
        if prefix:
            print(f"{prefix} {message}")
        else:
            print(message)
    
    def print_info(self, message: str) -> None:
        print(f"[info] {message}")
    
    def print_assistant_message(self, message: str) -> None:
        print(f"[assistant] {message}")
    
    async def get_user_input(self) -> str:
        try:
            return input("\n> ")
        except EOFError:
            return "/exit"
    
    def start_stream_display(self) -> None:
        pass
    
    def print_streaming_content(self, content: str) -> None:
        print(content, end="", flush=True)
    
    def stop_stream_display(self) -> None:
        print()
    
    def _format_args_summary(self, args: dict, max_len: int = 80) -> str:
        """Format args dict into a compact summary string."""
        if not args:
            return ""
        
        parts = []
        for key, value in args.items():
            val_str = str(value)
            # Truncate long values
            if len(val_str) > 50:
                val_str = val_str[:47] + "..."
            # Quote strings
            if isinstance(value, str):
                val_str = f'"{val_str}"'
            parts.append(f"{key}={val_str}")
        
        result = ", ".join(parts)
        if len(result) > max_len:
            result = result[:max_len - 3] + "..."
        return result
    
    def show_preparing_tool(self, name: str, args: dict) -> None:
        args_str = self._format_args_summary(args)
        if args_str:
            print(f"\n[tool] {name}({args_str})")
        else:
            print(f"\n[tool] {name}()")
    
    def show_tool_execution(self, name: str, args: dict, success: bool, result: str) -> None:
        status = "✓" if success else "✗"
        args_str = self._format_args_summary(args)
        if args_str:
            print(f"[tool] {name}({args_str}) {status}")
        else:
            print(f"[tool] {name}() {status}")
    
    async def wait_for_user_approval(self, content: str) -> Tuple[bool, str]:
        print(f"\n[APPROVAL REQUIRED]\n{content}")
        response = input("Approve? (y/n): ").strip().lower()
        return response in ("y", "yes"), response
    
    # Subagent visibility methods for debugging
    def subagent_start(self, agent_name: str, task: str) -> None:
        """Called when a subagent is spawned."""
        print(f"\n{'='*60}")
        print(f"◆ SUBAGENT HANDOFF: [{agent_name}]")
        print(f"{'='*60}")
        print(f"Task: {task}")
        print(f"{'-'*60}")
    
    def subagent_tool(self, agent_name: str, tool_name: str, args: dict) -> None:
        """Called when a subagent executes a tool."""
        print(f"  L [{agent_name}] {tool_name}")
        for key, value in args.items():
            val_str = str(value)
            if len(val_str) > 100:
                val_str = val_str[:100] + "..."
            print(f"      {key}: {val_str}")
    
    def subagent_tool_result(self, agent_name: str, tool_name: str, success: bool, result: str) -> None:
        """Called when a subagent tool completes."""
        status = "✓" if success else "✗"
        print(f"  L [{agent_name}] {status} {tool_name}")
        # Show truncated result
        if len(result) > 200:
            print(f"      Result: {result[:200]}...")
        else:
            print(f"      Result: {result}")
    
    def subagent_complete(self, agent_name: str, result: str) -> None:
        """Called when a subagent completes its task."""
        print(f"\n{'='*60}")
        print(f"◆ SUBAGENT COMPLETE: [{agent_name}]")
        print(f"{'='*60}")
        # Show result (truncated if very long)
        if len(result) > 500:
            print(f"{result[:500]}...")
            print(f"[... truncated {len(result) - 500} chars ...]")
        else:
            print(result)
        print(f"{'='*60}\n")


async def main():
    import argparse
    import os
    from src.agent.factory import AgentFactory
    from src.storage.session_storage import SessionStorage

    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="Run the coding agent")
    parser.add_argument(
        "--repo-path",
        "-r",
        type=str,
        default=None,
        help="Path to the repository to work in (also: REPO_PATH env var)",
    )
    parser.add_argument(
        "--session",
        "-s",
        type=str,
        default=None,
        help="Session ID to resume or create",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume the most recent session for this workspace",
    )
    parser.add_argument(
        "--list-sessions",
        action="store_true",
        help="List saved sessions and exit",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save session to disk",
    )
    args = parser.parse_args()

    storage = SessionStorage()

    # Handle --list-sessions
    if args.list_sessions:
        sessions = storage.list_sessions()
        if not sessions:
            print("No saved sessions found.")
        else:
            print(f"{'ID':<30} {'Title':<25} {'Workspace':<30} {'Updated'}")
            print("-" * 100)
            for s in sessions:
                session_id = s["id"][:28] + ".." if len(s["id"]) > 30 else s["id"]
                title = (s["title"] or "")[:23] + ".." if len(s.get("title", "") or "") > 25 else (s.get("title") or "Untitled")
                workspace = (s.get("workspace") or "")[:28] + ".." if len(s.get("workspace", "") or "") > 30 else (s.get("workspace") or "")
                updated = (s.get("updated_at") or "")[:19]
                print(f"{session_id:<30} {title:<25} {workspace:<30} {updated}")
        return

    # Determine working directory: CLI flag > env var > current dir
    repo_path = args.repo_path or os.environ.get("REPO_PATH", None)

    if repo_path:
        repo_path = os.path.abspath(os.path.expanduser(repo_path))
        if os.path.isdir(repo_path):
            os.chdir(repo_path)
            print(f"Working in: {repo_path}")
        else:
            print(f"Error: Directory not found: {repo_path}")
            sys.exit(1)

    workspace = repo_path or os.getcwd()

    # Determine session ID
    session_id = None

    if args.session:
        # Explicit session ID
        session_id = args.session
        if storage.session_exists(session_id):
            print(f"Resuming session: {session_id}")
        else:
            print(f"Creating new session: {session_id}")

    elif args.resume:
        # Resume most recent session for this workspace
        session_id = storage.get_latest_session(workspace)
        if session_id:
            print(f"Resuming session: {session_id}")
        else:
            print("No previous session found for this workspace. Starting new session.")
            session_id = storage.generate_session_id()

    else:
        # New session
        session_id = storage.generate_session_id()

    print(f"Session: {session_id}")
    print(f"Agent initialized. Type your message or /exit to quit.\n")

    ui = SimpleUI()

    # Create history_manager with session persistence built-in
    history_manager = AgentFactory.create_history_manager(
        ui_manager=ui,
        storage=storage if not args.no_save else None,
        session_id=session_id,
        workspace=workspace,
    )

    try:
        agent = AgentFactory.create_agent(
            ui_manager=ui,
            workspace_root=workspace,
            history_manager=history_manager,
        )

        # Use HistoryManager's flush callback for auto-save
        async def on_turn_complete():
            """Called after each turn to save state."""
            history_manager.flush()

        await agent.start_conversation(on_turn_complete=on_turn_complete)

    except KeyboardInterrupt:
        # Save on exit
        if not args.no_save and session_id:
            print("\nSaving session...")
            history_manager.flush()
        print("Goodbye!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

