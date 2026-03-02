import { useState, useEffect } from "react";
import { getSkaterSeasonStats, getSkaterRecentGames } from "../api/skater";
import type { SkaterData, SkaterGamePredictions } from "../types/skater";
import { getPlayerBasicInfo, getPlayerUpcomingGame } from "../api/player";

const MOCK_PREDICTIONS: SkaterGamePredictions = {
  goals: 0,
  assists: 0,
  points: 0,
};

export function useSkater(id: number) {
  const [data, setData] = useState<SkaterData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    Promise.all([
      getPlayerBasicInfo(id),
      getPlayerUpcomingGame(id),
      getSkaterSeasonStats(id),
      getSkaterRecentGames(id),
    ])
      .then(([playerInfo, upcomingGame, seasonStats, recentGames]) => {
        setData({
          ...playerInfo,
          upcomingGame,
          gamePredictions: MOCK_PREDICTIONS,
          seasonStats,
          recentGames,
        });
      })
      .catch(setError)
      .finally(() => setLoading(false));
  }, [id]);

  return { data, loading, error };
}