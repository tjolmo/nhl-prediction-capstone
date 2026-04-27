import { useState, useEffect } from "react";
import { getGoalieSeasonStats, getGoalieRecentGames, getGoaliePredictions } from "../api/goalie";
import { getPlayerBasicInfo, getPlayerUpcomingGame } from "../api/player";
import type { GoalieData } from "../types/goalie";

export function useGoalie(id: number) {
  const [data, setData] = useState<GoalieData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    Promise.all([
      getPlayerBasicInfo(id),
      getPlayerUpcomingGame(id).catch(() => null),
      getGoalieSeasonStats(id).catch(() => null),
      getGoalieRecentGames(id).catch(() => null),
      getGoaliePredictions(id).catch(() => null),
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