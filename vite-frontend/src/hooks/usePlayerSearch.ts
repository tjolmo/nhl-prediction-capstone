import { useState, useEffect } from "react";
import type { SearchPlayerResult } from "../types/player";
import { getSearchPlayer } from "../api/player";

export function usePlayerSearch(debounceMs: number = 300) {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<SearchPlayerResult[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!query.trim()) {
            setResults([]);
            setError(null);
            return;
        }

        setLoading(true);
        const timer = setTimeout(async () => {
            try {
                const data = await getSearchPlayer(query.trim(), 3);
                setResults(data);
                setError(null);
            } catch (e) {
                setError(e instanceof Error ? e.message : "Search failed");
                setResults([]);
            } finally {
                setLoading(false);
            }
        }, debounceMs);

        return () => {
            clearTimeout(timer);
            setLoading(false);
        };
    }, [query, debounceMs]);

    return { query, setQuery, results, loading, error };
}
