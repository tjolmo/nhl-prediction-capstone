import { useState, useEffect } from "react";
import type { TeamScheduledGame } from "../types/teams";
import { getGamesByDate } from "../api/games";

export function useDateGames(date: string) {
    const [data, setData] = useState<TeamScheduledGame[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        getGamesByDate(date)
            .then(setData)
            .catch(setError)
            .finally(() => setLoading(false));
    }, [date]);
    return { data, loading, error };
}