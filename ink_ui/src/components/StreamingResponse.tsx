import React from 'react'
import { Box, Text } from 'ink'

interface StreamingResponseProps {
    content: string
    width?: number
}

export const StreamingResponse: React.FC<StreamingResponseProps> = ({ content, width }) => {
    if (!content) return null

    const textWidth = width ? width - 4 : undefined

    return (
        <Box flexDirection="column" width={textWidth} marginBottom={1}>
            <Box flexDirection="row">
                <Text color="magentaBright">● </Text>
                <Text bold color="magentaBright">Agent</Text>
                <Text color="magentaBright"> ❯</Text>
            </Box>
            <Box marginLeft={2}>
                <Text wrap="wrap">{content}</Text>
                <Text color="cyan">▌</Text>
            </Box>
        </Box>
    )
}
