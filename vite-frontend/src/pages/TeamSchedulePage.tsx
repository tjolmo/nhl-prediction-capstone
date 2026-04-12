import { useParams } from "react-router-dom";
import { Link } from "react-router-dom";
import type { FC } from "react";
import { useEffect, useRef } from "react";
import { GameCard } from "../components/schedule/GameCard";
import { useTeamNextFive } from "../hooks/useTeamNextFive";
import type { TeamScheduledGame } from "../types/teams";
import LoadingPage from "./LoadingPage";
import ErrorPage from "./ErrorPage";

export const TeamSchedulePage: FC = () => {
  const { tricode } = useParams();
  const { games, loading, loadingMore, hasMore, loadMore, error } = useTeamNextFive(tricode!);
  const sentinelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const sentinel = sentinelRef.current;
    if (!sentinel) return;
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) loadMore();
      },
      { rootMargin: "200px" }
    );
    observer.observe(sentinel);
    return () => observer.disconnect();
  }, [loadMore]);

  if (error) return <ErrorPage message="Error loading team schedule data." />;
  if (loading) return <LoadingPage />;

  const nextGameDate = games.find((g: TeamScheduledGame) => g.isNextGame)?.date;

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
                Upcoming Schedule for {tricode}
              </h1>
              {nextGameDate && (
                <p className="text-blue-200 text-xs font-semibold mt-0.5">
                  Next game · {nextGameDate}
                </p>
              )}
            </div>
          </div>
          <div className="grid grid-cols-4 divide-x divide-slate-100 bg-slate-50 rounded-b-3xl">
            {[
              { label: "Games", value: games.length },
              { label: "Home", value: games.filter((g: TeamScheduledGame) => g.homeTeam.tricode === tricode).length },
              { label: "Away", value: games.filter((g: TeamScheduledGame) => g.awayTeam.tricode === tricode).length },
            ].map((s) => (
              <div key={s.label} className="py-3 text-center">
                <p className="text-lg font-black text-slate-800">{s.value}</p>
                <p className="text-[10px] font-semibold tracking-wider text-slate-400 uppercase">
                  {s.label}
                </p>
              </div>
            ))}
            <Link
              to={`/roster/${tricode}`}
              className="py-3 text-center flex flex-col items-center justify-center hover:bg-blue-50 transition-colors group"
            >
              <p className="text-lg font-black text-blue-600 group-hover:text-blue-700">→</p>
              <p className="text-[10px] font-semibold tracking-wider text-blue-500 uppercase">
                Roster
              </p>
            </Link>
          </div>
        </div>

        {games.map((game: TeamScheduledGame, i: number) => (
          <GameCard key={game.id} game={game} index={i} />
        ))}

        {hasMore && <div ref={sentinelRef} className="h-1" />}

        {loadingMore && (
          <div className="flex justify-center py-6">
            <div className="w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin" />
          </div>
        )}

        {!hasMore && games.length > 0 && (
          <p className="text-center text-slate-400 text-sm py-4">All Future Games Loaded</p>
        )}
      </div>
    </div>
  );
};

export default TeamSchedulePage;

