import { apiGet } from "./client";
import type { Team, TeamScheduledGame } from "../types/teams";
import type { PlayerFullData } from "../types/player";

export const getTeams = () =>
    apiGet<Team[]>("/teams/all");

export const getTeamNextFiveGames = (tricode: string) =>
    apiGet<TeamScheduledGame[]>(`/teams/${tricode}/next_5`);

export const getTeamCurrentRoster = (tricode: string) =>
    apiGet<PlayerFullData[]>(`/teams/${tricode}/current_roster`);