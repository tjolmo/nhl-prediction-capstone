import { apiGet } from "./client";
import type { PlayerData, UpcomingGame, SearchPlayerResult } from "../types/player";

export const getPlayerBasicInfo = (id: number) =>
    apiGet<Omit<PlayerData, "upcomingGame">>(`/players/player/${id}/basic_data`);

export const getPlayerUpcomingGame = (id: number) =>
    apiGet<UpcomingGame>(`/players/player/${id}/upcoming_game`);

export const getSearchPlayer = (query: string, limit: number = 10) =>
    apiGet<SearchPlayerResult[]>(`/players/search?q=${encodeURIComponent(query)}&limit=${limit}`);