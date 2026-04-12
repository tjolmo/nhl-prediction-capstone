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
    seasonSummary: { label: string; value: number | string }[];
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

export interface PlayerFullData {
    id: number;
    headshot: string;
    first_name: string;
    last_name: string;
    current_team_tri_code: string | null;
    position: Position;
    number: number | null;
    shoots_catches: "L" | "R";
    last_updated: string;
    game_log_last_updated: string | null;
}

export type Position = "C" | "L" | "R" | "D" | "G";

export interface PositionGroupConfig {
    key: Position;
    label: string;
    plural: string;
}

export interface PlayerCardProps {
    player: PlayerFullData;
    index: number;
}

export interface PositionGroupProps {
    label: string;
    players: PlayerFullData[];
    startIndex: number;
}

export interface SearchPlayerResult {
    id: number;
    first_name: string;
    last_name: string;
    headshot: string | null;
    current_team_tri_code: string | null;
    position: Position | null;
}