#!/bin/bash
# Terminal UI launcher
# Run from project root: ./terminal_ui/start.sh [--repo-path PATH]
#
# Usage:
#   ./terminal_ui/start.sh                    # Use current directory
#   ./terminal_ui/start.sh -r ~/my-project    # Specify repo path
#   REPO_PATH=~/my-project ./terminal_ui/start.sh  # Via env var

cd "$(dirname "$0")/.."

# Pass all arguments through
exec bun run ink_ui/src/index.tsx "$@"
