import { useState, useEffect } from "react";
import type { SearchPlayerResult } from "../types/player";
import type { SearchTeamResult } from "../types/teams";
import { getSearchPlayer } from "../api/player";
import { getSearchTeam } from "../api/teams";

export interface SearchResults {
    players: SearchPlayerResult[];
    teams: SearchTeamResult[];
}

export function useSearch(debounceMs: number = 300) {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<SearchResults>({ players: [], teams: [] });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const hasResults = results.players.length > 0 || results.teams.length > 0;

    useEffect(() => {
        if (!query.trim()) {
            setResults({ players: [], teams: [] });
            setError(null);
            return;
        }

        setLoading(true);
        const timer = setTimeout(async () => {
            try {
                const [players, teams] = await Promise.all([
                    getSearchPlayer(query.trim(), 3),
                    getSearchTeam(query.trim(), 3),
                ]);
                setResults({ players, teams });
                setError(null);
            } catch (e) {
                setError(e instanceof Error ? e.message : "Search failed");
                setResults({ players: [], teams: [] });
            } finally {
                setLoading(false);
            }
        }, debounceMs);

        return () => {
            clearTimeout(timer);
            setLoading(false);
        };
    }, [query, debounceMs]);

    return { query, setQuery, results, hasResults, loading, error };
}
