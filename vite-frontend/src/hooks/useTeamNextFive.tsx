import { useState, useEffect } from "react";
import type { TeamScheduledGame } from "../types/teams";
import { getTeamNextFiveGames } from "../api/teams";

export function useTeamNextFive(tricode: string) {
    const [data, setData] = useState<TeamScheduledGame[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        Promise.all([
            getTeamNextFiveGames(tricode),
        ])
            .then(([nextGames]) => {
                setData(nextGames);
            })
            .catch(setError)
            .finally(() => setLoading(false));
    }, [tricode]);
    return { data, loading, error };
}