import { Routes, Route, Navigate } from "react-router-dom";

import SkaterDashboard from "./pages/SkaterDashboard";
import GoalieDashboard from "./pages/GoalieDashboard";
import { SkaterPredictionPanel } from "./components/SkaterPredictionPanel";
import { SkaterRecentGames } from "./components/SkaterRecentGames";
import { GoaliePredictionPanel } from "./components/goalie/GoaliePredictionPanel";
import { GoalieRecentGames } from "./components/goalie/GoalieRecentGames";
import SchedulePage from "./pages/SchedulePage";
import RosterPage from "./pages/RosterPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/player/97/predictions" replace />} />

      <Route path="/player/:id" element={<SkaterDashboard />}>
        <Route index element={<Navigate to="predictions" replace />} />
        <Route path="predictions" element={<SkaterPredictionPanel />} />
        <Route path="recent" element={<SkaterRecentGames />} />
      </Route>

      <Route path="/goalie/:id" element={<GoalieDashboard />}>
        <Route index element={<Navigate to="predictions" replace />} />
        <Route path="predictions" element={<GoaliePredictionPanel />} />
        <Route path="recent" element={<GoalieRecentGames />} />
      </Route>

      <Route path="/schedule/:tricode" element={<SchedulePage />} />
      <Route path="/roster/:tricode" element={<RosterPage />} />
    </Routes>
  );
}