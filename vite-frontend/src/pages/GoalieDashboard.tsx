import { Outlet, useParams } from "react-router-dom";
import { PlayerHeader } from "../components/player/PlayerHeader";
import { PlayerUpcomingGame } from "../components/player/PlayerUpcomingGame";
import { PlayerDashboardTabs } from "../components/player/PlayerDashboardTabs";
import { PlayerDashboardLayout } from "../components/player/PlayerDashboardLayout";
import { useGoalie } from "../hooks/useGoalie";
import LoadingPage from "./LoadingPage";
import ErrorPage from "./ErrorPage";

const TABS = [
    { to: "predictions", label: "Predictions", icon: "🎯" },
    { to: "recent", label: "Recent Games", icon: "📊" },
];

export default function GoalieDashboard() {
    const { id } = useParams();
    const { data: goalieData, loading, error } = useGoalie(Number(id!));
    if (loading) return <LoadingPage />;
    if (error || !goalieData) return <ErrorPage message="Error loading player data." />;
    const { name, number, team, position, headshotUrl, upcomingGame, seasonStats } = goalieData!;

    const seasonSummary = [
        { label: "GP", value: seasonStats.games },
        { label: "SV%", value: (seasonStats.save_percentage * 100).toFixed(1) },
    ];

    return (
        <PlayerDashboardLayout>
            <PlayerHeader
                name={name}
                number={number}
                team={team}
                position={position}
                headshotUrl={headshotUrl}
                upcomingGame={upcomingGame}
                seasonSummary={seasonSummary}
            />
            <PlayerUpcomingGame upcomingGame={upcomingGame} />
            <PlayerDashboardTabs tabs={TABS} />
            <Outlet context={goalieData} />
        </PlayerDashboardLayout>
    );
}
