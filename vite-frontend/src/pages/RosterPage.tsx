import { useParams, Link } from "react-router-dom";
import type { FC } from "react";
import type { PlayerFullData, Position, PositionGroupConfig } from "../types/player";
import { PositionGroup } from "../components/roster/PositionGroup";
import { useRoster } from "../hooks/useRoster";
import LoadingPage from "./LoadingPage";
import ErrorPage from "./ErrorPage";

const POSITION_GROUPS: PositionGroupConfig[] = [
  { key: "C", label: "Centers", plural: "Centers" },
  { key: "L", label: "Left Wings", plural: "Left Wings" },
  { key: "R", label: "Right Wings", plural: "Right Wings" },
  { key: "D", label: "Defensemen", plural: "Defensemen" },
  { key: "G", label: "Goalies", plural: "Goalies" },
];

export const RosterPage: FC = () => {
  const { tricode } = useParams<{ tricode: string }>();
  const { data: players, loading, error } = useRoster(tricode!);
  if (loading) { return <LoadingPage />; }
  if (error) { return <ErrorPage message="Error loading roster data." />; }

  const grouped = POSITION_GROUPS.reduce<Record<Position, PlayerFullData[]>>(
    (acc, group) => {
      acc[group.key] = players
        ? players.filter((p) => p.position === group.key)
        : [];
      return acc;
    },
    { C: [], L: [], R: [], D: [], G: [] }
  );

  let cardIndex = 0;

  const totalPlayers = players?.length ?? 0;
  const totalSkaters = players?.filter((p) => p.position !== "G").length ?? 0;
  const totalGoalies = players?.filter((p) => p.position === "G").length ?? 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-100 font-sans p-4 sm:p-6 lg:p-10">
      <div className="fixed top-0 right-0 w-96 h-96 bg-blue-400/10 rounded-full blur-3xl pointer-events-none" />
      <div className="fixed bottom-0 left-0 w-64 h-64 bg-indigo-400/10 rounded-full blur-3xl pointer-events-none" />

      <div className="relative max-w-5xl mx-auto space-y-6">
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
                Team Roster
              </h1>
              {tricode && (
                <p className="text-blue-200 text-xs font-semibold mt-0.5 tracking-widest uppercase">
                  {tricode}
                </p>
              )}
            </div>
          </div>

          <div className="grid grid-cols-4 divide-x divide-slate-100 bg-slate-50 rounded-b-3xl">
            {loading ? (
              [0, 1, 2, 3].map((i) => (
                <div key={i} className="py-3 text-center">
                  <div className="h-6 w-8 bg-slate-200 rounded-lg mx-auto animate-pulse" />
                  <div className="h-3 w-14 bg-slate-100 rounded-lg mx-auto mt-1.5 animate-pulse" />
                </div>
              ))
            ) : (
              <>
                {[
                  { label: "Players", value: totalPlayers },
                  { label: "Skaters", value: totalSkaters },
                  { label: "Goalies", value: totalGoalies },
                ].map((s) => (
                  <div key={s.label} className="py-3 text-center">
                    <p className="text-lg font-black text-slate-800">{s.value}</p>
                    <p className="text-[10px] font-semibold tracking-wider text-slate-400 uppercase">
                      {s.label}
                    </p>
                  </div>
                ))}
                <Link
                  to={`/schedule/team/${tricode}`}
                  className="py-3 text-center flex flex-col items-center justify-center hover:bg-blue-50 transition-colors group"
                >
                  <p className="text-lg font-black text-blue-600 group-hover:text-blue-700">→</p>
                  <p className="text-[10px] font-semibold tracking-wider text-blue-500 uppercase">
                    Schedule
                  </p>
                </Link>
              </>
            )}
          </div>
        </div>

        {loading ? (
          <div className="space-y-6">
            {POSITION_GROUPS.map((group) => (
              <div key={group.key} className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className="h-4 w-24 bg-slate-200 rounded-lg animate-pulse" />
                  <div className="flex-1 h-px bg-slate-200" />
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
                  {Array.from({
                    length: group.key === "D" ? 4 : group.key === "G" ? 2 : 3,
                  }).map((_, i) => (
                    <div
                      key={i}
                      className="rounded-2xl bg-white shadow-lg shadow-slate-200/50 h-44 animate-pulse"
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="space-y-6">
            {POSITION_GROUPS.map((group) => {
              const groupPlayers = grouped[group.key];
              const start = cardIndex;
              cardIndex += groupPlayers.length;
              return (
                <PositionGroup
                  key={group.key}
                  label={group.label}
                  players={groupPlayers}
                  startIndex={start}
                />
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default RosterPage;
