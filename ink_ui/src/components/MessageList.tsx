import React from 'react'
import { Box, Text, TextProps } from 'ink'
import { Message } from '../types.js'
import { MessageBubble, MessageBubbleVariant } from './MessageBubble.js'

interface MessageListProps {
    messages: Message[]
    width?: number
}

type MessagePreset = {
    label: string
    color: TextProps['color']
    variant: MessageBubbleVariant
    icon: string
}

const MESSAGE_PRESETS: Record<Message['type'], MessagePreset> = {
    user: { label: 'You', color: 'cyanBright', variant: 'solid', icon: '>' },
    agent: { label: 'Agent', color: 'magentaBright', variant: 'solid', icon: '●' },
    system: { label: 'System', color: 'gray', variant: 'ghost', icon: '◇' },
    error: { label: 'Error', color: 'redBright', variant: 'solid', icon: '⚠' },
    tool: { label: 'Tool', color: 'blueBright', variant: 'solid', icon: '⌘' }
}

// Render tool message with tree-like structure
const ToolMessage: React.FC<{ content: string; width?: number }> = ({ content, width }) => {
    const textWidth = width ? width - 4 : undefined

    // Check if it starts with status indicator
    const isSuccess = content.startsWith('✓')
    const isFailure = content.startsWith('✗')

    if (isSuccess || isFailure) {
        const statusColor = isSuccess ? 'green' : 'red'
        return (
            <Box width={textWidth}>
                <Text color={statusColor}>{content.charAt(0)} </Text>
                <Text wrap="wrap">{content.slice(2)}</Text>
            </Box>
        )
    }

    // Tool preparing format: ● ToolName(args)
    return (
        <Box flexDirection="column" width={textWidth}>
            <Text color="blueBright">⌘ </Text>
            <Text wrap="wrap">{content}</Text>
        </Box>
    )
}

export const MessageList: React.FC<MessageListProps> = ({ messages, width }) => {
    // Show all messages except system (shown elsewhere)
    const visibleMessages = messages.filter(msg => msg.type !== 'system')

    return (
        <Box flexDirection="column">
            {visibleMessages.map((msg, idx) => (
                <Box key={idx} marginBottom={1}>
                    {msg.type === 'tool' ? (
                        <ToolMessage content={msg.content} width={width} />
                    ) : (
                        <MessageBubble
                            label={MESSAGE_PRESETS[msg.type].label}
                            color={MESSAGE_PRESETS[msg.type].color}
                            content={msg.content}
                            variant={MESSAGE_PRESETS[msg.type].variant}
                            icon={MESSAGE_PRESETS[msg.type].icon}
                            width={width}
                        />
                    )}
                </Box>
            ))}
        </Box>
    )
}
