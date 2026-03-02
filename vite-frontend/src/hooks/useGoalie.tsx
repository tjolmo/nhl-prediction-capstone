import { useState, useEffect } from "react";
import { getGoalieSeasonStats, getGoalieRecentGames } from "../api/goalie";
import { getPlayerBasicInfo, getPlayerUpcomingGame } from "../api/player";
import type { GoalieData, GoalieGamePredictions } from "../types/goalie";

const MOCK_PREDICTIONS: GoalieGamePredictions = {
    saves: 0,
    goals_against: 0,
};

export function useGoalie(id: number) {
  const [data, setData] = useState<GoalieData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    Promise.all([
      getPlayerBasicInfo(id),
      getPlayerUpcomingGame(id),
      getGoalieSeasonStats(id),
      getGoalieRecentGames(id),
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