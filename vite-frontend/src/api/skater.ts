import { apiGet } from "./client";
import type {  SkaterSeasonStats, SkaterGameStats } from "../types/skater";

export const getSkaterSeasonStats = (id: number) =>
    apiGet<SkaterSeasonStats>(`/players/skater/${id}/basic_stats/2025`); // current season

export const getSkaterRecentGames = (id: number) =>
    apiGet<SkaterGameStats[]>(`/players/skater/${id}/last_5/basic_stats`);
