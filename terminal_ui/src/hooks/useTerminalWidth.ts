import { useState, useEffect } from 'react'

export const useTerminalWidth = () => {
    const [width, setWidth] = useState(process.stdout.columns || 80)

    useEffect(() => {
        const handleResize = () => {
            setWidth(process.stdout.columns || 80)
        }

        process.stdout.on('resize', handleResize)
        return () => {
            process.stdout.off('resize', handleResize)
        }
    }, [])

    return width
}
