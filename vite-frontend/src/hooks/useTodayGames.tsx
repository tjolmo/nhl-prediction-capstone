import { useState, useEffect } from "react";
import type { TeamScheduledGame } from "../types/teams";
import { getTodaysGames } from "../api/games";

export function useTodayGames() {
    const [data, setData] = useState<TeamScheduledGame[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        Promise.all([
            getTodaysGames()
        ])
            .then(([nextGames]) => {
                setData(nextGames);
            })
            .catch(setError)
            .finally(() => setLoading(false));
    }, []);
    return { data, loading, error };
}