import type { ReactNode } from "react";

export interface UpcomingGame {
    date: string;
    opposing_team_tricode: string;
    venue: string;
    time: Date;
    home_away: "HOME" | "AWAY";
}

export interface PlayerData {
    name: string;
    number: number;
    team: string;
    position: string;
    headshotUrl: string;
    upcomingGame: UpcomingGame;
}

export interface PlayerHeaderProps extends PlayerData {
    seasonSummary: {label: string; value: number|string}[];
}

export interface PlayerUpcomingGameProps {
    upcomingGame: UpcomingGame;

}
export interface PlayerPredictionCardProps {
  label: string;
  value: number | string;
  icon: string;
  color: string;
  bgColor: string;
  subtext: ReactNode;
}