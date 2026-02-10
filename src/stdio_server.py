#!/usr/bin/env python3
import asyncio
import os
import sys

from src.core import (
    Runner,
    AgentConfig,
    AgentRole,
    LegacyToolAdapter,
    create_llm,
    Session,
    combine,
    Event,
    Span,
)
from src.core.transports.stdio import StdioTransport
from src.tools.manager import ToolManager


from dotenv import load_dotenv

load_dotenv()


MAIN_PROMPT = """You are an expert software engineer. You help users understand and modify code.

When you need to explore or search the codebase, delegate to the 'explorer' agent.
When you have enough information, answer the user's question directly.

Be concise but thorough."""

EXPLORER_PROMPT = """You are a codebase explorer. Your job is to find and analyze code.

Use ripgrep to search for patterns, glob to find files, and read_file to examine code.
When you have gathered enough information, summarize your findings clearly.

Do NOT delegate - you ARE the explorer. Just search and report back."""


async def main():
    workspace = os.environ.get("REPO_PATH", os.getcwd())

    sys.stderr.write(f"Stdio server starting\n")
    sys.stderr.write(f"Workspace: {workspace}\n")
    sys.stderr.write(f"Model: {os.getenv('MODEL_NAME', 'gpt-4o')}\n")
    sys.stderr.flush()

    llm = create_llm()

    tool_manager = ToolManager(workspace_root=workspace)
    tool_manager.get_tools_description()
    tools = [LegacyToolAdapter(t) for t in tool_manager.tools.values()]

    stdio = StdioTransport()
    session = Session.new()
    handler = combine(stdio.handle, session.handle)

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
                    "read_file",
                    "edit_file",
                    "search_replace",
                    "delete_file",
                    "list_dir",
                    "ripgrep",
                    "glob",
                    "git_status",
                    "git_diff",
                    "git_commit",
                    "add_memory",
                    "list_memories",
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
                    "ripgrep",
                    "glob",
                    "read_file",
                    "list_dir",
                    "extract_symbols",
                    "get_context",
                    "repo_structure",
                ],
                max_turns=20,
            ),
        },
        handler=handler,
        human_input_fn=stdio.human_input_fn,
        approve=stdio.approval_fn,
    )

    sys.stderr.write(f"Ready. Listening on stdin...\n")
    sys.stderr.flush()

    from src.core.models import EventType

    await stdio._write_event(
        Event(
            type=EventType.ENVIRONMENT_INFO,
            span=Span(),
            data={"working_directory": workspace},
        )
    )

    current_task = None

    try:
        async for message in stdio.read_stdin():
            method = message.get("method")
            params = message.get("params", {})
            msg_id = message.get("id")

            try:
                if method == "run":
                    task = params.get("task", "")
                    if current_task and not current_task.done():
                        current_task.cancel()
                    current_task = asyncio.create_task(runner.run(task))
                    result = await current_task
                    await stdio.send_response(msg_id, {"output": result})

                elif method == "continue":
                    user_input = params.get("input", "")
                    if current_task and not current_task.done():
                        current_task.cancel()
                    current_task = asyncio.create_task(runner.continue_with(user_input))
                    result = await current_task
                    await stdio.send_response(msg_id, {"output": result})

                elif method == "respond":
                    request_id = params.get("request_id")
                    stdio.handle_response(request_id, params)
                    await stdio.send_response(msg_id, {"ok": True})

                elif method == "end_session":
                    if current_task and not current_task.done():
                        current_task.cancel()
                    await runner.end_session()
                    await stdio.send_response(
                        msg_id, {"session_path": str(session.path)}
                    )

                else:
                    await stdio.send_error(
                        msg_id,
                        StdioTransport.JSONRPC_METHOD_NOT_FOUND,
                        f"Method not found: {method}",
                    )

            except asyncio.CancelledError:
                await stdio.send_response(msg_id, {"output": "cancelled"})
            except Exception as e:
                await stdio.send_error(
                    msg_id, StdioTransport.JSONRPC_SERVER_ERROR, str(e)
                )

    except KeyboardInterrupt:
        if current_task and not current_task.done():
            current_task.cancel()
        await runner.end_session()
        sys.stderr.write(f"\nSession saved: {session.path}\n")


if __name__ == "__main__":
    asyncio.run(main())
