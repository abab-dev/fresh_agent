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
    
    def show_preparing_tool(self, name: str, args: dict) -> None:
        print(f"\n[tool] {name}")
    
    def show_tool_execution(self, name: str, args: dict, success: bool, result: str) -> None:
        status = "✓" if success else "✗"
        print(f"[tool] {name} {status}")
    
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
    
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="Run the coding agent")
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
            print(f"Working in: {repo_path}")
        else:
            print(f"Error: Directory not found: {repo_path}")
            sys.exit(1)
    
    print(f"Agent initialized. Type your message or /exit to quit.\n")
    
    ui = SimpleUI()
    
    # Determine workspace - use repo_path if set, otherwise cwd
    workspace = repo_path or os.getcwd()
    
    try:
        agent = AgentFactory.create_agent(ui_manager=ui, workspace_root=workspace)
        await agent.start_conversation()
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

