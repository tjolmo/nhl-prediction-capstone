import { useState, useEffect } from "react";
import type { PlayerFullData } from "../types/player";
import { getTopSkaters } from "../api/player";

export function useTopSkaters(season: number, n: number) {
    const [data, setData] = useState<PlayerFullData[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        getTopSkaters(season, n)
            .then(setData)
            .catch(setError)
            .finally(() => setLoading(false));
    }, [season, n]);
    return { data, loading, error };
}