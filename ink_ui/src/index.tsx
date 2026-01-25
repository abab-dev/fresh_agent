#!/usr/bin/env bun
import React from 'react'
import { render } from 'ink'
import App from './App.js'

// Check if stdin supports raw mode (real TTY)
const isTTY = process.stdin.isTTY

if (!isTTY) {
    console.log('Terminal UI requires a TTY. Run directly in a terminal.')
    console.log('Usage: bun run terminal_ui/src/index.tsx')
    process.exit(1)
}

render(<App />, {
    exitOnCtrlC: true
})
