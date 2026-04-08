import { apiGet } from "./client";
import type { TeamScheduledGame } from "../types/teams";

export const getGamesByDate = (date: string) =>
    apiGet<TeamScheduledGame[]>(`/teams/games/${date}`);