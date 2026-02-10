import { useInput, useApp, type Key } from 'ink'
import { AppMode } from '../types.js'

interface KeyboardOptions {
    mode: AppMode
    onStop: () => void
    onApprove: () => void
    onDeny: () => void
    onToggleArgs: () => void
}

export const useKeyboard = (opts: KeyboardOptions) => {
    const { exit } = useApp()
    const { mode, onStop, onApprove, onDeny, onToggleArgs } = opts

    useInput((input: string, key: Key) => {
        // Escape to exit
        if (key.escape) {
            exit()
            return
        }

        // Ctrl+S to stop agent
        if (key.ctrl && input === 's') {
            onStop()
            return
        }

        // Approval mode shortcuts
        if (mode === 'approval') {
            if (input === 'y' || input === 'Y') onApprove()
            if (input === 'n' || input === 'N') onDeny()
            if (input === 'a' || input === 'A') onToggleArgs()
        }
    })
}
