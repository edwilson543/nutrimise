import {useEffect} from "react";

/**
 * Execute a callback whenever some key is pressed.
 * */
export const useKeyboardShortcuts = (shortcuts: Record<string, () => void>) => {
    useEffect(() => {
        const handleKeyDown = (event: KeyboardEvent) => {
            if (shortcuts[event.key]) {
                event.preventDefault();
                shortcuts[event.key]();
            }
        };

        document.addEventListener('keydown', handleKeyDown);

        return () => {
            document.removeEventListener('keydown', handleKeyDown);
        };
    }, [shortcuts]);
}
