export interface Team {
  tricode: string;
  name: string;
  logoUrl: string;
}

export interface PredictedScore {
  away: number;
  home: number;
}

export interface TeamScheduledGame {
  id: number;
  date: string;
  time: string;
  venue: string;
  awayTeam: Team;
  homeTeam: Team;
  predictedScore: PredictedScore;
  isNextGame?: boolean;
}

export interface SearchTeamResult {
  name: string;
  tricode: string;
  logoUrl: string | null;
}