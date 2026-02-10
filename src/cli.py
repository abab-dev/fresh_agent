#!/usr/bin/env python3
"""CLI entry point for the agent."""

from dotenv import load_dotenv
load_dotenv()

import asyncio
import os
import sys

from src.core import (
    Runner, AgentConfig, AgentRole,
    LegacyToolAdapter, create_llm,
    Logger, Session, combine,
)
from src.tools.manager import ToolManager


# =============================================================================
# PROMPTS
# =============================================================================

MAIN_PROMPT = """You are an expert software engineer. You help users understand and modify code.

When you need to explore or search the codebase, delegate to the 'explorer' agent.
When you have enough information, answer the user's question directly.

Be concise but thorough."""

EXPLORER_PROMPT = """You are a codebase explorer. Your job is to find and analyze code.

Use ripgrep to search for patterns, glob to find files, and read_file to examine code.
When you have gathered enough information, summarize your findings clearly.

Do NOT delegate - you ARE the explorer. Just search and report back."""


# =============================================================================
# MAIN
# =============================================================================

async def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run the coding agent")
    parser.add_argument(
        "--repo-path", "-r", type=str, default=None,
        help="Path to the repository to work in (also: REPO_PATH env var)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", default=True,
        help="Verbose logging (default: on)",
    )
    args = parser.parse_args()

    # Determine workspace
    repo_path = args.repo_path or os.environ.get("REPO_PATH", None)
    if repo_path:
        repo_path = os.path.abspath(os.path.expanduser(repo_path))
        if os.path.isdir(repo_path):
            os.chdir(repo_path)
        else:
            print(f"Error: Directory not found: {repo_path}")
            sys.exit(1)

    workspace = repo_path or os.getcwd()
    model = os.getenv("MODEL_NAME", "gpt-4o")

    print(f"Workspace: {workspace}")
    print(f"Model: {model}")

    # LLM
    llm = create_llm()

    # Adapt existing tools
    tool_manager = ToolManager(workspace_root=workspace)
    tool_manager.get_tools_description()  # Force lazy load
    tools = [LegacyToolAdapter(t) for t in tool_manager.tools.values()]

    # Event handlers
    logger = Logger(verbose=args.verbose)
    session = Session.new()
    handler = combine(logger.handle, session.handle)

    # Runner with explicit agent registry
    runner = Runner.create(
        llm=llm,
        tools=tools,
        agents={
            "main": AgentConfig(
                name="main",
                role=AgentRole.MAIN,
                system_prompt=MAIN_PROMPT,
                allowed_tools=[
                    "cmd_runner",
                    "read_file", "edit_file", "search_replace", "delete_file", "list_dir",
                    "ripgrep", "glob",
                    "git_status", "git_diff", "git_commit",
                    "add_memory", "list_memories",
                    "scratchpad",
                    "delegate",
                ],
                max_turns=50,
            ),
            "explorer": AgentConfig(
                name="explorer",
                role=AgentRole.SUBAGENT,
                system_prompt=EXPLORER_PROMPT,
                allowed_tools=[
                    "ripgrep", "glob", "read_file", "list_dir",
                    "extract_symbols", "get_context", "repo_structure",
                ],
                max_turns=20,
            ),
        },
        handler=handler,
    )

    print(f"Agents: {runner.registered_agents}")
    print(f"Tools: {[t.name for t in tools]}")
    print(f"Session: {session.path}")
    print(f"\nReady. Type your message or Ctrl+C to exit.\n")

    # Conversation loop
    try:
        first_turn = True
        while True:
            try:
                user_input = input("> ").strip()
            except EOFError:
                break

            if not user_input:
                continue
            if user_input.lower() in ("/exit", "/quit", "exit", "quit"):
                break

            try:
                if first_turn:
                    result = await runner.run(user_input)
                    first_turn = False
                else:
                    result = await runner.continue_with(user_input)

                print(f"\n{result}\n")
            except Exception as e:
                print(f"\n[Error] {e}\n")

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    finally:
        await runner.end_session()
        print(f"Session saved: {session.path}")


if __name__ == "__main__":
    asyncio.run(main())
