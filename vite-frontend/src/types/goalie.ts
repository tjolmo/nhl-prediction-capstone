import type { PlayerData } from "./player";

export interface GoalieGamePredictions {
  saves: number;
  goals_against: number;
}

export interface GoalieSeasonStats {
  save_percentage: number;
  gaa: number;
  games: number;
}

export interface GoalieGameStats {
  date: string;
  opposing_team_tricode: string;
  saves: number;
  save_percentage: number;
  goals_against: number;
  home_away: "HOME" | "AWAY";
}

export interface GoalieData extends PlayerData {
  gamePredictions: GoalieGamePredictions;
  seasonStats: GoalieSeasonStats;
  recentGames: GoalieGameStats[];
}

export interface GoalieGameRowProps {
  game_stats: GoalieGameStats;
  index: number;
}

export type GoalieStatKey = "saves" | "goals_against" | "save_percentage";