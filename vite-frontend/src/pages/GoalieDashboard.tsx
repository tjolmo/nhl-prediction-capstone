import { Outlet, useParams } from "react-router-dom";
import { PlayerDashboardLayout } from "../components/PlayerDashboardLayout";
import { PlayerHeader } from "../components/PlayerHeader";
import { PlayerUpcomingGame } from "../components/PlayerUpcomingGame";
import { PlayerDashboardTabs } from "../components/PlayerDashboardTabs";
import { useGoalie } from "../hooks/useGoalie";

const TABS = [
    { to: "predictions", label: "Predictions", icon: "🎯" },
    { to: "recent", label: "Recent Games", icon: "📊" },
];

export default function GoalieDashboard() {
    const { id } = useParams();
    const { data: goalieData, loading, error } = useGoalie(Number(id!));
    if (error || !goalieData) return <div>Error loading player data.</div>;
    if (loading) return <div>Loading...</div>;
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
