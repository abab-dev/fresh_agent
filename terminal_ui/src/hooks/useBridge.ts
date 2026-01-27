import { useState, useEffect, useRef } from 'react'
import { spawn, ChildProcess } from 'child_process'
import { useApp } from 'ink'
import { AppMode, Message, ToolRequest, BridgeMessage, Todo } from '../types.js'

export const useBridge = () => {
    const [mode, setMode] = useState<AppMode>('loading')
    const [messages, setMessages] = useState<Message[]>([])
    const [currentResponse, setCurrentResponse] = useState('')
    const [workingDir, setWorkingDir] = useState('')
    const [pendingTool, setPendingTool] = useState<ToolRequest | null>(null)
    const [statusLine, setStatusLine] = useState('')
    const [todos, setTodos] = useState<Todo[]>([])

    const processRef = useRef<ChildProcess | null>(null)
    const stoppingRef = useRef(false)
    const { exit } = useApp()

    const pythonCmd = process.env.PYTHON || 'python3'

    const send = (msg: BridgeMessage) => {
        if (processRef.current?.stdin?.writable) {
            processRef.current.stdin.write(JSON.stringify(msg) + '\n')
        }
    }

    const appendMessage = (type: Message['type'], content?: unknown) => {
        const text = typeof content === 'string' ? content.trim() : ''
        if (!text) return
        setMessages(prev => [...prev, { type, content: text }])
    }

    const finalizeResponse = (fallback = '') => {
        setCurrentResponse(prev => {
            const final = (prev + fallback).replace(/^[\n\r]+/, '')
            if (final) {
                // Defer to avoid render loop issues
                setTimeout(() => {
                    setMessages(msgs => [...msgs, { type: 'agent', content: final }])
                }, 0)
            }
            return ''
        })
    }

    const handleMessage = (msg: BridgeMessage) => {
        const { type, data } = msg

        switch (type) {
            case 'ready':
                setMode('ready')
                break

            case 'environment_info':
                setWorkingDir((data.working_directory as string) || '')
                break

            case 'thinking':
                setMode('thinking')
                setStatusLine('Thinking')
                break

            case 'stream_chunk':
                setMode('responding')
                setCurrentResponse(prev => {
                    const next = prev + (data.content as string)
                    return prev === '' ? next.replace(/^\n+/, '') : next
                })
                break

            case 'stream_end':
                finalizeResponse((data.content as string) || '')
                setMode('thinking') // Transition out of responding immediately
                setStatusLine('')
                break

            case 'input_request':
                setMode('ready')
                setStatusLine('Waiting for input...')
                break

            case 'tool_request':
                setPendingTool({ name: data.name as string, args: data.args as string })
                setMode('approval')
                break

            case 'tool_executing':
                setMode('executing')
                setStatusLine(`> ${data.name}`)
                break

            case 'tool_preparing': {
                setMode('executing')
                const args = (data.args || {}) as Record<string, unknown>
                const summary = Object.entries(args)
                    .slice(0, 4)  // Max 4 args shown
                    .map(([k, v]) => {
                        const val = typeof v === 'string'
                            ? `"${v.length > 40 ? v.slice(0, 37) + '...' : v}"`
                            : String(v).slice(0, 40)
                        return `${k}=${val}`
                    })
                    .join(', ')
                const argsDisplay = summary + (Object.keys(args).length > 4 ? ', ...' : '')
                setStatusLine(`> ${data.name}(${argsDisplay})`)
                appendMessage('tool', `● ${data.name}(${argsDisplay})`)
                break
            }

            case 'tool_result': {
                const name = (data.name as string) || 'tool'
                const success = data.success as boolean | undefined
                const args = (data.args || {}) as Record<string, unknown>
                const status = success === false ? '✗' : '✓'

                // Compact args for result line
                const argKeys = Object.keys(args).slice(0, 2)
                const argsHint = argKeys.length > 0
                    ? argKeys.map(k => {
                        const v = args[k]
                        const val = typeof v === 'string' ? v.slice(0, 20) : String(v).slice(0, 15)
                        return `${k}=${val}`
                    }).join(', ')
                    : ''

                // Show result preview for failures
                let resultPreview = ''
                if (success === false) {
                    const result = typeof data.result === 'string' ? data.result : JSON.stringify(data.result)
                    resultPreview = `: ${result.slice(0, 100)}`
                }

                appendMessage('tool', `${status} ${name}(${argsHint})${resultPreview}`)
                setStatusLine('')
                break
            }

            case 'turn_status': {
                const state = (data.state as string) || ''
                setStatusLine(state)
                break
            }

            case 'stream_start':
                setMode('responding')
                setStatusLine('Responding')
                setCurrentResponse('')
                break

            case 'complete':
            case 'interrupted':
            case 'stopped':
                setMode('ready')
                setStatusLine('')
                if (type === 'stopped') {
                    setMessages(prev => [...prev, { type: 'system', content: '[x] Agent stopped' }])
                    setCurrentResponse('')
                    setPendingTool(null)
                    stoppingRef.current = false
                }
                break

            case 'error':
                appendMessage('error', (data.message as string) || (data.error as string))
                setMode('ready')
                break

            case 'message': {
                const content = data.content as string
                appendMessage('system', content)
                break
            }

            case 'assistant_message':
                finalizeResponse(data.content as string)
                break

            case 'info':
                appendMessage('system', data.content as string)
                break

            // Subagent events
            case 'subagent_start': {
                const agent = data.agent as string
                const task = data.task as string
                const taskPreview = task.length > 100 ? task.slice(0, 100) + '...' : task
                appendMessage('tool', `◆ [${agent}] Started: ${taskPreview}`)
                setStatusLine(`[${agent}] running...`)
                break
            }

            case 'subagent_tool': {
                const agent = data.agent as string
                const name = data.name as string
                const args = (data.args || {}) as Record<string, unknown>
                const argSummary = Object.entries(args)
                    .slice(0, 3)
                    .map(([k, v]) => `${k}=${typeof v === 'string' ? v.slice(0, 30) : v}`)
                    .join(', ')
                appendMessage('tool', `  L [${agent}] ${name}(${argSummary})`)
                break
            }

            case 'subagent_tool_result': {
                const agent = data.agent as string
                const name = data.name as string
                const success = data.success as boolean
                const result = (data.result as string) || ''
                const status = success ? '✓' : '✗'
                const preview = result.length > 100 ? result.slice(0, 100) + '...' : result
                appendMessage('tool', `  L [${agent}] ${status} ${name}: ${preview}`)
                break
            }

            case 'subagent_complete': {
                const agent = data.agent as string
                const result = (data.result as string) || ''
                const preview = result.length > 200 ? result.slice(0, 200) + '...' : result
                appendMessage('tool', `◆ [${agent}] Complete: ${preview}`)
                setStatusLine('')
                break
            }

            // Todo events
            case 'todo_update': {
                const todoList = (data.todos as Todo[]) || []
                setTodos(todoList)
                break
            }
        }
    }

    useEffect(() => {
        // Spawn the Python bridge
        processRef.current = spawn(pythonCmd, ['-m', 'src.bridge_ui'], {
            stdio: ['pipe', 'pipe', 'pipe'],
            cwd: process.cwd()
        })

        let buffer = ''

        processRef.current.stdout?.on('data', (chunk: Buffer) => {
            buffer += chunk.toString()
            const regex = /__MSG__(.*?)__END__/g
            let match

            while ((match = regex.exec(buffer)) !== null) {
                try {
                    const msg = JSON.parse(match[1]) as BridgeMessage
                    handleMessage(msg)
                } catch (e) {
                    // Ignore parse errors
                }
            }

            const lastEnd = buffer.lastIndexOf('__END__')
            if (lastEnd !== -1) buffer = buffer.slice(lastEnd + 7)
        })

        processRef.current.stderr?.on('data', (chunk: Buffer) => {
            // Log stderr for debugging
            const text = chunk.toString().trim()
            if (text) {
                appendMessage('error', text)
            }
        })

        processRef.current.on('close', () => exit())

        return () => { processRef.current?.kill() }
    }, [])

    const sendUserInput = (message: string) => {
        setMessages(prev => [...prev, { type: 'user', content: message }])
        setMode('thinking')
        send({ type: 'user_input', data: { message } })
    }

    const sendApproval = (approved: boolean, content = '') => {
        send({ type: 'tool_approval', data: { approved, content } })
        setPendingTool(null)
        setMode(approved ? 'executing' : 'ready')
        if (!approved) {
            setMessages(prev => [...prev, { type: 'system', content: `[x] Denied: ${pendingTool?.name}` }])
        }
    }

    const stopAgent = () => {
        if (!stoppingRef.current) {
            stoppingRef.current = true
            send({ type: 'stop_agent', data: {} })
            setCurrentResponse('')
            setPendingTool(null)
        }
    }

    return {
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
    }
}
