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


async def main():
    from src.agent.factory import AgentFactory
    
    print("Agent initialized. Type your message or /exit to quit.\n")
    
    ui = SimpleUI()
    
    try:
        agent = AgentFactory.create_agent(ui_manager=ui)
        await agent.start_conversation()
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
