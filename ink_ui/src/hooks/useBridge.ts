import { useState, useEffect, useRef } from 'react'
import { spawn, ChildProcess } from 'child_process'
import { useApp } from 'ink'
import { AppMode, Message, ToolRequest } from '../types.js'

interface StdioEvent {
    type: string
    span: { run_id: string; agent: string; depth: number }
    data: Record<string, unknown>
    timestamp: string
}

interface JsonRpcResponse {
    jsonrpc: string
    id: number
    result?: unknown
    error?: { code: number; message: string }
}

export const useBridge = () => {
    const [mode, setMode] = useState<AppMode>('loading')
    const [messages, setMessages] = useState<Message[]>([])
    const [currentResponse, setCurrentResponse] = useState('')
    const [workingDir, setWorkingDir] = useState(process.cwd())
    const [pendingTool, setPendingTool] = useState<ToolRequest | null>(null)
    const [statusLine, setStatusLine] = useState('')
    const [isFirstMessage, setIsFirstMessage] = useState(true)

    const processRef = useRef<ChildProcess | null>(null)
    const messageIdRef = useRef(0)
    const pendingInputRef = useRef<{ requestId: string; resolve: (value: string) => void } | null>(null)
    const { exit } = useApp()

    const pythonCmd = process.env.PYTHON || 'python3'

    const send = (method: string, params: Record<string, unknown> = {}) => {
        if (processRef.current?.stdin?.writable) {
            const message = {
                method,
                params,
                id: ++messageIdRef.current,
            }
            processRef.current.stdin.write(JSON.stringify(message) + '\n')
        }
    }

    const appendMessage = (type: Message['type'], content: string) => {
        if (!content.trim()) return
        setMessages(prev => [...prev, { type, content: content.trim() }])
    }

    const finalizeStreamingResponse = () => {
        setCurrentResponse(prev => {
            if (prev.trim()) {
                setTimeout(() => {
                    setMessages(msgs => [...msgs, { type: 'agent', content: prev }])
                }, 0)
            }
            return ''
        })
    }

    const handleEvent = (event: StdioEvent) => {
        const { type, data, span } = event
        const indent = '  '.repeat(span.depth)
        const agentLabel = span.depth > 0 ? `[${span.agent}]` : ''

        switch (type) {
            case 'workflow_start':
                setMode('thinking')
                break

            case 'agent_start':
                if (span.depth > 0) {
                    appendMessage('tool', `${indent}◆ ${agentLabel} → ${(data.task as string || '').slice(0, 100)}`)
                }
                setStatusLine(`${agentLabel} thinking...`)
                break

            case 'agent_end':
                if (span.depth > 0) {
                    const output = (data.output as string || '').slice(0, 200)
                    appendMessage('tool', `${indent}◆ ${agentLabel} ✓ ${output}`)
                }
                setStatusLine('')
                break

            case 'llm_start':
                setMode('thinking')
                setStatusLine(`${agentLabel} thinking...`)
                break

            case 'llm_stream_start':
                setMode('responding')
                setCurrentResponse('')
                break

            case 'llm_stream_chunk':
                setMode('responding')
                const chunk = data.content as string || ''
                setCurrentResponse(prev => {
                    const next = prev + chunk
                    return prev === '' ? next.replace(/^\n+/, '') : next
                })
                break

            case 'llm_end':
                const tokens = data.tokens as number || 0
                setStatusLine(`${agentLabel} (${tokens} tokens)`)
                // Finalize streaming response if we were streaming
                if (mode === 'responding') {
                    finalizeStreamingResponse()
                }
                break

            case 'tool_start':
                setMode('executing')
                const toolName = data.name as string
                const args = (data.args || {}) as Record<string, unknown>
                setStatusLine(`${agentLabel} ${toolName}...`)

                // Show tool with arguments
                const argSummary = Object.entries(args)
                    .slice(0, 3)
                    .map(([k, v]) => `${k}=${typeof v === 'string' ? v.slice(0, 40) : JSON.stringify(v).slice(0, 40)}`)
                    .join(', ')
                appendMessage('tool', `${indent}🔧 ${toolName}(${argSummary})`)
                break

            case 'tool_end':
                const name = data.name as string
                const success = data.success as boolean
                const duration = data.duration_ms as number || 0
                const status = success ? '✓' : '✗'
                appendMessage('tool', `${indent}${status} ${name} (${duration}ms)`)
                break

            case 'delegation_start':
                appendMessage('tool', `${indent}📤 → ${data.agent}`)
                setStatusLine(`${agentLabel} delegating to ${data.agent}...`)
                break

            case 'delegation_end':
                appendMessage('tool', `${indent}📥 ← done`)
                setStatusLine('')
                break

            case 'human_input_waiting':
                setMode('ready')
                setStatusLine('Waiting for your input...')
                const requestId = data.request_id as string
                // Store for later response
                pendingInputRef.current = {
                    requestId,
                    resolve: (response: string) => {
                        send('respond', { request_id: requestId, response })
                        pendingInputRef.current = null
                    }
                }
                break

            case 'human_input_received':
                setMode('thinking')
                setStatusLine('')
                break

            case 'approval_required':
                setMode('approval')
                setPendingTool({
                    name: data.tool as string,
                    args: JSON.stringify(data.args || {}, null, 2),
                    requestId: data.request_id as string,
                })
                break

            case 'tool_denied':
                appendMessage('system', `🚫 Denied: ${data.tool}`)
                setPendingTool(null)
                setMode('ready')
                break

            case 'workflow_end':
                setMode('ready')
                setStatusLine('')
                // Don't show output here - it came from JSON-RPC response
                break

            case 'environment_info':
                setWorkingDir((data.working_directory as string) || process.cwd())
                break
        }
    }

    const handleResponse = (response: JsonRpcResponse) => {
        if (response.error) {
            appendMessage('error', response.error.message)
            setMode('ready')
        }
        // Don't show output from result - it should have streamed already via llm_stream_chunk
        // Just acknowledge completion
        setMode('ready')
    }

    useEffect(() => {
        // Spawn stdio server
        processRef.current = spawn(pythonCmd, ['-m', 'src.stdio_server'], {
            stdio: ['pipe', 'pipe', 'pipe'],
            cwd: process.cwd(),
        })

        let buffer = ''

        processRef.current.stdout?.on('data', (chunk: Buffer) => {
            buffer += chunk.toString()
            const lines = buffer.split('\n')
            buffer = lines.pop() || ''

            for (const line of lines) {
                if (!line.trim()) continue

                try {
                    const parsed = JSON.parse(line)

                    // Check if it's a JSON-RPC response or an event
                    if ('jsonrpc' in parsed && 'id' in parsed) {
                        handleResponse(parsed as JsonRpcResponse)
                    } else if ('type' in parsed && 'span' in parsed) {
                        handleEvent(parsed as StdioEvent)
                    }
                } catch {
                    // Ignore parse errors
                }
            }
        })

        processRef.current.stderr?.on('data', (chunk: Buffer) => {
            const text = chunk.toString().trim()
            if (text) {
                // Stderr is for server logs
                console.error('[server]', text)
            }
        })

        processRef.current.on('close', () => exit())

        // Initial ready state
        setTimeout(() => setMode('ready'), 500)

        return () => {
            send('end_session')
            processRef.current?.kill()
        }
    }, [])

    const sendUserInput = (message: string) => {
        setMessages(prev => [...prev, { type: 'user', content: message }])
        setMode('thinking')

        // Check if this is a response to a pending input request
        if (pendingInputRef.current) {
            pendingInputRef.current.resolve(message)
        } else {
            // New run or continue - use isFirstMessage flag
            if (isFirstMessage) {
                send('run', { task: message })
                setIsFirstMessage(false)
            } else {
                send('continue', { input: message })
            }
        }
    }

    const sendApproval = (approved: boolean) => {
        if (!pendingTool) return

        const requestId = pendingTool.requestId
        if (requestId) {
            send('respond', { request_id: requestId, approved })
        }

        setPendingTool(null)
        setMode(approved ? 'executing' : 'ready')

        if (!approved) {
            appendMessage('system', `[x] Denied: ${pendingTool.name}`)
        }
    }

    const stopAgent = () => {
        send('end_session')
        setCurrentResponse('')
        setPendingTool(null)
        setMode('ready')
        setIsFirstMessage(true)  // Reset for new conversation
    }

    return {
        mode,
        messages,
        currentResponse,
        workingDir,
        pendingTool,
        statusLine,
        sendUserInput,
        sendApproval,
        stopAgent,
    }
}
