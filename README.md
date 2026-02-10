# Fresh Agent

A coding assistant that runs in your terminal.

## What it does

- Reads, edits, and searches your code
- Runs shell commands
- Uses Git
- Delegates complex tasks to specialized sub-agents
- Remembers things across conversations

## Install

```bash
uv pip install -e .
```

## Setup

Create a `.env` file:

```bash
OPENAI_API_KEY=your-key-here
MODEL_NAME=gpt-4o
```

Or use any LiteLLM-compatible provider:

```bash
OPENAI_BASE_URL=https://your-provider.com/v1
MODEL_NAME=openai/gpt-4o
```

## Run

```bash
python main.py
```

This starts a terminal UI. Type your request and press Enter.

## How it works

The agent uses a **ReAct loop**: it thinks, calls tools, reads results, and repeats until done.

### Core components

- **Runner**: Manages the agent lifecycle and handles delegation
- **Agent**: Runs the think-act loop until it finishes
- **Tools**: Read files, run commands, search code, etc.
- **Streaming**: LLM responses stream in real-time

### Agent delegation

The main agent can delegate to specialized sub-agents:

- **explorer**: Deep code search and analysis

Add more agents in `stdio_server.py` by registering them with the Runner.

## Architecture

```
src/
├── core/
│   ├── runner.py       # Orchestrates agents and handles intents
│   ├── agent.py        # ReAct loop (think → act → observe)
│   ├── llm.py          # LiteLLM client with streaming
│   ├── tools.py        # Tool execution and approval
│   ├── models.py       # Data structures and events
│   ├── events.py       # Event system for UI updates
│   ├── delegation.py   # Delegation tool
│   └── transports/
│       └── stdio.py    # JSON-RPC transport for UI
├── tools/
│   ├── filesystem/     # read, edit, delete files
│   ├── search/         # ripgrep, glob, file search
│   ├── code/           # symbol extraction, context
│   ├── git/            # status, diff, commit
│   ├── memory/         # persistent notes
│   └── utilities/      # scratchpad
├── cli.py              # Terminal interface
└── stdio_server.py     # JSON-RPC server for Ink UI

ink_ui/
└── src/
    ├── App.tsx         # Main React component
    ├── hooks/
    │   └── useBridge.ts  # Backend communication
    └── components/     # UI elements
```

## Events

The agent emits events as it works. The UI listens and updates in real-time.

Key events:
- `WORKFLOW_START` / `WORKFLOW_END`
- `LLM_START` / `LLM_STREAM_CHUNK` / `LLM_END`
- `TOOL_START` / `TOOL_END`
- `DELEGATION_START` / `DELEGATION_END`
- `HUMAN_INPUT_WAITING`

## Tools

| Tool | What it does |
|------|--------------|
| `read_file` | Read file contents |
| `edit_file` | Create or modify files |
| `search_replace` | Find and replace in files |
| `delete_file` | Delete files/directories |
| `list_dir` | List directory contents |
| `cmd_runner` | Run shell commands |
| `ripgrep` | Fast text search |
| `glob` | Find files by pattern |
| `grep_search` | Search in files |
| `file_search` | Find files by name |
| `extract_symbols` | Get code structure |
| `get_context` | Get code context |
| `repo_structure` | Show repo tree |
| `git_status` | Git status |
| `git_diff` | Show changes |
| `git_commit` | Commit changes |
| `add_memory` | Save a note |
| `list_memories` | List saved notes |
| `scratchpad` | Agent's thinking space |
| `delegate` | Hand off to another agent |

## Development

Run with environment variables:

```bash
REPO_PATH=/path/to/your/code python main.py
```

The agent will work in that directory.

## License

MIT
