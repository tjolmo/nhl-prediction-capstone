import type { FC } from "react";
import { GameCard } from "../components/schedule/GameCard";
import { useParams, useNavigate } from "react-router-dom";
import { useDateGames } from "../hooks/useDateGames";
import LoadingPage from "./LoadingPage";
import ErrorPage from "./ErrorPage";

const toDateParam = (d: Date): string => {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}${m}${day}`;
};

const parseDate = (date: string): Date => {
  if (date === "today") return new Date();
  return new Date(
    parseInt(date.substring(0, 4)),
    parseInt(date.substring(4, 6)) - 1,
    parseInt(date.substring(6, 8))
  );
};

export const DailySchedulePage: FC = () => {
  const { date } = useParams();
  const navigate = useNavigate();
  const { data: games, loading, error } = useDateGames(date!);

  const currentDate = parseDate(date!);

  const goYesterday = () => {
    const prev = new Date(currentDate);
    prev.setDate(prev.getDate() - 1);
    navigate(`/schedule/${toDateParam(prev)}`);
  };

  const goTomorrow = () => {
    const next = new Date(currentDate);
    next.setDate(next.getDate() + 1);
    navigate(`/schedule/${toDateParam(next)}`);
  };

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
            <button
              onClick={goYesterday}
              aria-label="Go to yesterday's schedule"
              className="absolute left-4 top-1/2 -translate-y-1/2 z-10 flex items-center justify-center w-9 h-9 rounded-full bg-white/20 hover:bg-white/35 active:scale-95 transition-all duration-150 text-white shadow"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5">
                <path fillRule="evenodd" d="M11.78 5.22a.75.75 0 0 1 0 1.06L8.06 10l3.72 3.72a.75.75 0 1 1-1.06 1.06l-4.25-4.25a.75.75 0 0 1 0-1.06l4.25-4.25a.75.75 0 0 1 1.06 0Z" clipRule="evenodd" />
              </svg>
            </button>

            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <h1 className="text-white font-black text-2xl tracking-tight drop-shadow">
                {date === "today"
                  ? `Today (${new Date().toLocaleDateString()})`
                  : currentDate.toLocaleDateString()}
                's Schedule
              </h1>
            </div>

            <button
              onClick={goTomorrow}
              aria-label="Go to tomorrow's schedule"
              className="absolute right-4 top-1/2 -translate-y-1/2 z-10 flex items-center justify-center w-9 h-9 rounded-full bg-white/20 hover:bg-white/35 active:scale-95 transition-all duration-150 text-white shadow"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5">
                <path fillRule="evenodd" d="M8.22 5.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.75.75 0 1 1-1.06-1.06L11.94 10 8.22 6.28a.75.75 0 0 1 0-1.06Z" clipRule="evenodd" />
              </svg>
            </button>
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
