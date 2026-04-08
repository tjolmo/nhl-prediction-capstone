import type { FC } from "react";
import { GameCard } from "../components/schedule/GameCard";
import { useParams } from "react-router-dom";
import { useDateGames } from "../hooks/useDateGames";
import LoadingPage from "./LoadingPage";
import ErrorPage from "./ErrorPage";

export const DailySchedulePage: FC = () => {
  const { date } = useParams();
  const { data: games, loading, error } = useDateGames(date!);
  if (loading) return <LoadingPage />;
  if (error || !games) return <ErrorPage message="Error loading schedule data." />;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-100 font-sans p-4 sm:p-6 lg:p-10">
      <div className="fixed top-0 right-0 w-96 h-96 bg-blue-400/10 rounded-full blur-3xl pointer-events-none" />
      <div className="fixed bottom-0 left-0 w-64 h-64 bg-indigo-400/10 rounded-full blur-3xl pointer-events-none" />
      <div className="relative max-w-2xl mx-auto space-y-4">
        <div className="bg-white rounded-3xl shadow-xl shadow-slate-200/60 overflow-hidden">
          <div className="h-20 bg-gradient-to-r from-blue-700 via-blue-600 to-indigo-700 relative">
            <div
              className="absolute inset-0 opacity-20"
              style={{
                backgroundImage:
                  "repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,.15) 10px, rgba(255,255,255,.15) 11px)",
              }}
            />
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <h1 className="text-white font-black text-2xl tracking-tight drop-shadow">
                {date === 'today'
                  ? `Today (${new Date().toLocaleDateString()})`
                  : new Date(
                    parseInt(date!.substring(0, 4)),
                    parseInt(date!.substring(4, 6)) - 1,
                    parseInt(date!.substring(6, 8))
                  ).toLocaleDateString()}
                's Schedule
              </h1>
            </div>
          </div>
        </div>
        {games.map((game, i) => (
          <GameCard key={game.id} game={game} index={i} />
        ))}
      </div>
    </div>
  );
};

export default DailySchedulePage;
