import { apiGet } from "./client";
import type { TeamScheduledGame } from "../types/teams";

export const getTodaysGames = () =>
    apiGet<TeamScheduledGame[]>("/teams/games/today");