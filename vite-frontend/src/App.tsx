import { Routes, Route, Navigate } from "react-router-dom";

import SkaterDashboard from "./pages/SkaterDashboard";
import GoalieDashboard from "./pages/GoalieDashboard";
import { SkaterPredictionPanel } from "./components/skater/SkaterPredictionPanel";
import { SkaterRecentGames } from "./components/skater/SkaterRecentGames";
import { GoaliePredictionPanel } from "./components/goalie/GoaliePredictionPanel";
import { GoalieRecentGames } from "./components/goalie/GoalieRecentGames";
import TeamSchedulePage from "./pages/TeamSchedulePage";
import RosterPage from "./pages/RosterPage";
import DailySchedulePage from "./pages/DailySchedulePage";
import TeamsPage from "./pages/TeamsPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/schedule/today" />} />

      <Route path="/player/:id" element={<SkaterDashboard />}>
        <Route index element={<Navigate to="predictions" />} />
        <Route path="predictions" element={<SkaterPredictionPanel />} />
        <Route path="recent" element={<SkaterRecentGames />} />
      </Route>

      <Route path="/goalie/:id" element={<GoalieDashboard />}>
        <Route index element={<Navigate to="predictions" />} />
        <Route path="predictions" element={<GoaliePredictionPanel />} />
        <Route path="recent" element={<GoalieRecentGames />} />
      </Route>

      <Route path="/schedule/team/:tricode" element={<TeamSchedulePage />} />
      <Route path="/schedule/:date" element={<DailySchedulePage />} />
      <Route path="/roster/:tricode" element={<RosterPage />} />
      <Route path="/teams" element={<TeamsPage />} />
    </Routes>
  );
}