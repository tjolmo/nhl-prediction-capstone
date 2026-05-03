import type { PlayerData, PlayerPropData } from "./player";

export interface SkaterGamePredictions {
  goals: number;
  assists: number;
  points: number;
  prob_goal: number;
  prob_assist: number;
  prob_point: number;
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

export interface SkaterData extends PlayerData {
  gamePredictions: SkaterGamePredictions;
  seasonStats: SkaterSeasonStats;
  recentGames: SkaterGameStats[];
  playerProps: PlayerPropData[];
}

export interface SkaterGameRowProps {
  game_stats: SkaterGameStats;
  index: number;
}

export type SkaterStatKey = "goals" | "assists" | "points";