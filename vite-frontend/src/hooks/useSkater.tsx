import { useState, useEffect } from "react";
import { getSkaterSeasonStats, getSkaterRecentGames, getSkaterPredictions } from "../api/skater";
import type { SkaterData } from "../types/skater";
import { getPlayerBasicInfo, getPlayerUpcomingGame } from "../api/player";

export function useSkater(id: number) {
  const [data, setData] = useState<SkaterData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    Promise.all([
      getPlayerBasicInfo(id),
      getPlayerUpcomingGame(id).catch(() => null),
      getSkaterSeasonStats(id).catch(() => null),
      getSkaterRecentGames(id).catch(() => null),
      getSkaterPredictions(id).catch(() => null),
    ])
      .then(([playerInfo, upcomingGame, seasonStats, recentGames, gamePredictions]) => {
        setData({
          ...playerInfo,
          upcomingGame: upcomingGame!,
          gamePredictions: gamePredictions!,
          seasonStats: seasonStats!,
          recentGames: recentGames!,
        });
      })
      .catch(setError)
      .finally(() => setLoading(false));
  }, [id]);

  return { data, loading, error };
}