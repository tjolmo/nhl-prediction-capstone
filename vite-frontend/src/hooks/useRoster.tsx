import { useState, useEffect } from "react";
import type { PlayerFullData } from "../types/player";
import { getTeamCurrentRoster } from "../api/teams";

export const useRoster = (tricode: string) => {
  const [data, setData] = useState<PlayerFullData[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    Promise.all([
      getTeamCurrentRoster(tricode)
    ])
      .then(([roster]) => {
        setData(roster);
      })
      .catch(setError)
      .finally(() => setLoading(false));
  }, [tricode]);

  return { data, loading, error };
};
