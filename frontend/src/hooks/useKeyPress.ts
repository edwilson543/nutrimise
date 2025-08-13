import {useEffect} from "react";

/**
 * Execute a callback whenever some key is pressed
 * */
export const useKeyPress = (key: string, callback: () => void) => {
    useEffect(() => {
        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key === key) {
                callback();
            }
        };

        document.addEventListener('keydown', handleKeyDown);

        return () => {
            document.removeEventListener('keydown', handleKeyDown);
        };
    }, [key, callback]);
}
