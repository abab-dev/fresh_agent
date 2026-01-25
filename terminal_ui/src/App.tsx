import React, { useState, useEffect } from 'react'
import { Box, Text } from 'ink'
import { Header } from './components/Header.js'
import { MessageList } from './components/MessageList.js'
import { StreamingResponse } from './components/StreamingResponse.js'
import { Spinner } from './components/Spinner.js'
import { InputBox } from './components/InputBox.js'
import { TodoList } from './components/TodoList.js'
import { useBridge } from './hooks/useBridge.js'
import { useTerminalWidth } from './hooks/useTerminalWidth.js'
import { useKeyboard } from './hooks/useKeyboard.js'

const Divider: React.FC<{ width: number }> = ({ width }) => {
    const length = Math.max(24, Math.min(width - 4, 80))
    return <Text dimColor color="gray">{'─'.repeat(length)}</Text>
}

const App: React.FC = () => {
    const [input, setInput] = useState('')
    const [showToolArgs, setShowToolArgs] = useState(false)

    const {
        mode,
        messages,
        currentResponse,
        workingDir,
        pendingTool,
        statusLine,
        todos,
        sendUserInput,
        sendApproval,
        stopAgent
    } = useBridge()

    const width = useTerminalWidth()

    useKeyboard({
        mode,
        onStop: stopAgent,
        onApprove: () => sendApproval(true),
        onDeny: () => sendApproval(false),
        onToggleArgs: () => setShowToolArgs(s => !s)
    })

    useEffect(() => {
        // Clear screen and hide cursor on mount
        process.stdout.write('\x1Bc')
        process.stdout.write('\x1B[?25l')
        return () => { process.stdout.write('\x1B[?25h') }
    }, [])

    const handleSubmit = () => {
        const msg = input.trim()
        if (!msg) return
        sendUserInput(msg)
        setInput('')
    }

    const queuedCount = messages.filter(m => m.queued).length

    if (mode === 'loading') {
        return (
            <Box flexDirection="column" padding={2}>
                <Spinner label="Initializing agent..." />
            </Box>
        )
    }

    return (
        <Box flexDirection="column" paddingX={2}>
            <Header workingDirectory={workingDir} terminalWidth={width} />

            <Box flexDirection="column" marginBottom={1}>
                {todos.length > 0 && <TodoList todos={todos} />}
                <MessageList messages={messages} width={width} />
                <StreamingResponse content={currentResponse} width={width} />
                {(mode === 'thinking' || mode === 'executing') && !currentResponse && (
                    <Spinner label={statusLine} />
                )}
            </Box>

            <Divider width={width} />

            <InputBox
                mode={mode}
                value={input}
                onChange={setInput}
                onSubmit={handleSubmit}
                queuedCount={queuedCount}
                pendingTool={pendingTool}
                showToolArgs={showToolArgs}
            />
        </Box>
    )
}

export default App
