import React from 'react'
import { Box, Text } from 'ink'

interface Todo {
    id: number
    content: string
    status: 'pending' | 'in_progress' | 'completed'
}

interface TodoListProps {
    todos: Todo[]
}

const STATUS_ICONS: Record<Todo['status'], { icon: string; color: string }> = {
    pending: { icon: '○', color: 'gray' },
    in_progress: { icon: '▶', color: 'yellow' },
    completed: { icon: '✓', color: 'green' }
}

export const TodoList: React.FC<TodoListProps> = ({ todos }) => {
    if (!todos || todos.length === 0) return null

    const completed = todos.filter(t => t.status === 'completed').length
    const total = todos.length

    return (
        <Box
            flexDirection="column"
            borderStyle="round"
            borderColor="blue"
            paddingX={1}
            marginBottom={1}
        >
            {/* Header */}
            <Box marginBottom={1}>
                <Text bold color="blue">◆ Tasks </Text>
                <Text color="gray">({completed}/{total} complete)</Text>
            </Box>

            {/* Task list */}
            <Box flexDirection="column">
                {todos.map(todo => {
                    const { icon, color } = STATUS_ICONS[todo.status]
                    const textColor = todo.status === 'completed' ? 'gray' : undefined
                    const dimmed = todo.status === 'completed'

                    return (
                        <Box key={todo.id}>
                            <Text color={color}>{icon} </Text>
                            <Text color={textColor} dimColor={dimmed}>
                                {todo.content}
                            </Text>
                            {todo.status === 'in_progress' && (
                                <Text color="yellow" dimColor> (working)</Text>
                            )}
                        </Box>
                    )
                })}
            </Box>
        </Box>
    )
}
