# Autonomous Coding Agent

A modular, extensible framework for building autonomous coding agents with LLM backends.

## Features

- **Recursive Agentic Loop**: Automatically handles tool calls until task completion
- **Modular Tool System**: Lazy-loaded tools with registry pattern
- **Context Management**: Automatic compression and LLM-based summarization
- **History Tracking**: Full conversation history with token usage monitoring
- **Memory Persistence**: Store and recall important information across sessions
- **Sub-agents**: Specialized agents for code review, testing, refactoring, and debugging

## Installation

```bash
# Install dependencies
pip install -e .

# Or with uv
uv pip install -e .
```

## Configuration

Set your API key and optionally configure the model:

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://api.openai.com/v1"  # Optional, for other providers
export MODEL_NAME="gpt-4o"  # Optional, default is gpt-4o
export MODEL_MAX_TOKENS="200"  # Optional, in thousands (200 = 200k)
```

## Usage

### CLI

```bash
python main.py
```

### Programmatic

```python
import asyncio
from src.agent.factory import AgentFactory

class MyUI:
    # Implement UIProtocol methods...
    pass

async def main():
    ui = MyUI()
    agent = AgentFactory.create_agent(ui_manager=ui)
    await agent.start_conversation()

asyncio.run(main())
```

## Architecture

```
src/
├── agent/          # Core agent orchestration
│   ├── agent.py    # Main Agent class with recursive loop
│   ├── client.py   # LLM API client with streaming
│   ├── executor.py # Tool execution logic
│   ├── factory.py  # Component factory
│   └── ...
├── tools/          # Tool implementations
│   ├── filesystem/ # File operations
│   ├── execution/  # Shell commands
│   ├── search/     # Grep, file search
│   ├── git/        # Git operations
│   ├── memory/     # Persistent notes
│   └── utilities/  # Todos, scratchpad
├── prompts/        # Prompt management
├── history/        # Conversation tracking
├── subagents/      # Specialized sub-agents
└── utils/          # Shared utilities
```

## Available Tools

| Tool | Description |
|------|-------------|
| `read_file` | Read file contents with line ranges |
| `edit_file` | Create or overwrite files |
| `search_replace` | Find and replace in files |
| `delete_file` | Delete files/directories |
| `list_dir` | List directory contents |
| `cmd_runner` | Execute shell commands |
| `grep_search` | Search for patterns in files |
| `file_search` | Find files by name |
| `git_status` | Get repository status |
| `git_diff` | Show changes |
| `git_commit` | Commit changes |
| `add_memory` | Store persistent notes |
| `list_memories` | Retrieve stored notes |
| `todo_write` | Manage todo list |
| `scratchpad` | Thinking workspace |

## Project Instructions

Create an `AGENT.md` file in your project root to provide project-specific instructions to the agent.

## License

MIT
