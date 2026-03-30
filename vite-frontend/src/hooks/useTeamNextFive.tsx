import { useState, useEffect, useCallback } from "react";
import type { TeamScheduledGame } from "../types/teams";
import { getTeamNextFiveGames } from "../api/teams";

const PAGE_SIZE = 5;

export function useTeamNextFive(tricode: string) {
    const [games, setGames] = useState<TeamScheduledGame[]>([]);
    const [offset, setOffset] = useState(0);
    const [loading, setLoading] = useState(true);
    const [loadingMore, setLoadingMore] = useState(false);
    const [hasMore, setHasMore] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        setLoading(true);
        setGames([]);
        setOffset(0);
        setHasMore(true);
        getTeamNextFiveGames(tricode, 0)
            .then((nextGames) => {
                setGames(nextGames);
                if (nextGames.length < PAGE_SIZE) setHasMore(false);
                else setOffset(PAGE_SIZE);
            })
            .catch(setError)
            .finally(() => setLoading(false));
    }, [tricode]);

    const loadMore = useCallback(() => {
        if (loadingMore || !hasMore) return;
        setLoadingMore(true);
        getTeamNextFiveGames(tricode, offset)
            .then((nextGames) => {
                setGames((prev) => [...prev, ...nextGames]);
                if (nextGames.length < PAGE_SIZE) setHasMore(false);
                else setOffset((prev) => prev + PAGE_SIZE);
            })
            .catch(setError)
            .finally(() => setLoadingMore(false));
    }, [tricode, offset, loadingMore, hasMore]);

    return { games, loading, loadingMore, hasMore, loadMore, error };
}