import React from 'react'
import { Box, Text, TextProps } from 'ink'

export type MessageBubbleVariant = 'solid' | 'ghost'

interface MessageBubbleProps {
    label: string
    color?: TextProps['color']
    content: string
    meta?: string
    variant?: MessageBubbleVariant
    icon?: string
    width?: number
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({
    label,
    color = 'gray',
    content,
    meta,
    variant = 'solid',
    icon,
    width
}) => {
    const contentColor: TextProps['color'] | undefined = variant === 'ghost' ? 'gray' : undefined
    const isMultiline = content.includes('\n')
    const textWidth = width ? width - 4 : undefined

    // For multiline content, render header separately
    if (isMultiline) {
        return (
            <Box flexDirection="column" width={textWidth}>
                <Box flexDirection="row">
                    <Text>
                        {icon && <Text color={color}>{icon} </Text>}
                        <Text bold color={color}>{label}</Text>
                        <Text color={color}> ❯</Text>
                        {meta && (
                            <Text dimColor color={variant === 'ghost' ? 'gray' : color}> · {meta}</Text>
                        )}
                    </Text>
                </Box>
                <Box marginLeft={2}>
                    <Text color={contentColor} wrap="wrap">{content}</Text>
                </Box>
            </Box>
        )
    }

    // Single line
    return (
        <Box width={textWidth}>
            <Text wrap="wrap">
                {icon && <Text color={color}>{icon} </Text>}
                <Text bold color={color}>{label}</Text>
                <Text color={color}> ❯</Text>
                {meta && (
                    <Text dimColor color={variant === 'ghost' ? 'gray' : color}> · {meta}</Text>
                )}
                <Text color={contentColor}> {content}</Text>
            </Text>
        </Box>
    )
}
