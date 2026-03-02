import {apiGet} from "./client";
import type { TeamScheduledGame } from "../types/teams";

export const getTeamNextFiveGames = (tricode: string) =>
    apiGet<TeamScheduledGame[]>(`/teams/${tricode}/next_5`);