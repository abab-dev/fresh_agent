import React, { memo } from 'react'
import { Box, Text } from 'ink'

interface HeaderProps {
    workingDirectory: string
    terminalWidth: number
}

const truncatePath = (path: string, maxLen: number): string => {
    if (path.length <= maxLen) return path
    const parts = path.split('/')
    if (parts.length <= 2) return path.slice(-maxLen)
    return '~/' + parts.slice(-2).join('/')
}

// Simple ASCII art logo
const LOGO_WIDE = [
    '   ___                    __  ',
    '  /   | ____ ____  ____  / /_ ',
    ' / /| |/ __ `/ _ \\/ __ \\/ __/ ',
    '/ ___ / /_/ /  __/ / / / /_   ',
    '/_/  |_\\__, /\\___/_/ /_/\\__/  ',
    '      /____/                   '
]

const LOGO_NARROW = 'AGENT'

export const Header: React.FC<HeaderProps> = memo(({ workingDirectory, terminalWidth }) => {
    const isWide = terminalWidth >= 80

    return (
        <Box flexDirection="column" marginBottom={1}>
            <Box
                flexDirection="row"
                borderStyle="round"
                borderColor="cyan"
                paddingX={1}
            >
                {/* Left side - Logo */}
                <Box flexDirection="column" marginRight={2}>
                    {isWide ? (
                        LOGO_WIDE.map((line, i) => (
                            <Text key={i} color="cyan">{line}</Text>
                        ))
                    ) : (
                        <Text bold color="cyan">{LOGO_NARROW}</Text>
                    )}
                    <Text dimColor color="gray">your coding assistant</Text>
                    {workingDirectory && (
                        <Text color="yellow" dimColor>
                            {truncatePath(workingDirectory, isWide ? 40 : 20)}
                        </Text>
                    )}
                </Box>

                {/* Right side - Tips */}
                <Box flexDirection="column" borderLeft borderColor="gray" paddingLeft={2}>
                    <Text bold color="green">Tips for getting started</Text>
                    <Text dimColor>Type a message to start coding</Text>
                    <Text> </Text>
                    <Text bold color="yellow">Shortcuts</Text>
                    <Text dimColor>Esc: exit | Ctrl+S: stop | y/n: approve/deny</Text>
                </Box>
            </Box>
        </Box>
    )
})

Header.displayName = 'Header'
