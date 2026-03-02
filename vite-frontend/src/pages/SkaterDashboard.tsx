import { Outlet, useParams } from "react-router-dom";
//import { skaterData } from "../data/mockSkaterData";
import { PlayerDashboardLayout } from "../components/PlayerDashboardLayout";
import { PlayerHeader } from "../components//PlayerHeader";
import { PlayerUpcomingGame } from "../components/PlayerUpcomingGame";
import { PlayerDashboardTabs } from "../components/PlayerDashboardTabs";
import { useSkater } from "../hooks/useSkater";

const TABS = [
  { to: "predictions", label: "Predictions", icon: "🎯" },
  { to: "recent", label: "Recent Games", icon: "📊" },
];


export default function SkaterDashboard() {
  const { id } = useParams();
  const { data: skaterData, loading, error } = useSkater(Number(id!));
  if (error || !skaterData) return <div>Error loading player data.</div>;
  if (loading) return <div>Loading...</div>;
  const { name, number, team, position, headshotUrl, upcomingGame, seasonStats } = skaterData!;
  const seasonSummary = [
    { label: "GP", value: seasonStats.games },
    { label: "G", value: seasonStats.goals },
    { label: "A", value: seasonStats.assists },
    { label: "PTS", value: seasonStats.points },
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
      <Outlet context={skaterData} />
    </PlayerDashboardLayout>
  );
}
