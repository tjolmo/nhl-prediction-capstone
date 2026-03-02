import type { PlayerData } from "./player";

export interface SkaterGamePredictions {
  goals: number;
  assists: number;
  points: number;
}

export interface SkaterSeasonStats {
  goals: number;
  assists: number;
  points: number;
  games: number;
}

export interface SkaterGameStats {
  date: string;
  opposing_team_tricode: string;
  goals: number;
  assists: number;
  points: number;
  home_away: "HOME" | "AWAY";
}

export interface SkaterData extends PlayerData{
  gamePredictions: SkaterGamePredictions;
  seasonStats: SkaterSeasonStats;
  recentGames: SkaterGameStats[];
}

export interface SkaterGameRowProps {
  game_stats: SkaterGameStats;
  index: number;
}

export type SkaterStatKey = "goals" | "assists" | "points";