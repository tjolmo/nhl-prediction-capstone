import { useState, useEffect } from "react";
import { getTeams } from "../api/teams";
import type { Team } from "../types/teams";

export const useTeams = () => {
  const [data, setData] = useState<Team[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    getTeams()
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  return { data, loading, error };
};
