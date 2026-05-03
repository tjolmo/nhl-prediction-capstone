import { useParams, Link } from "react-router-dom";
import type { FC } from "react";
import type { PlayerFullData, Position, PositionGroupConfig } from "../types/player";
import { PositionGroup } from "../components/roster/PositionGroup";
import { useRoster } from "../hooks/useRoster";
import LoadingPage from "./LoadingPage";
import ErrorPage from "./ErrorPage";

const POSITION_GROUPS: PositionGroupConfig[] = [
  { key: "C", label: "Center", plural: "Centers" },
  { key: "L", label: "Left Wing", plural: "Left Wings" },
  { key: "R", label: "Right Wing", plural: "Right Wings" },
  { key: "D", label: "Defenseman", plural: "Defensemen" },
  { key: "G", label: "Goalie", plural: "Goalies" },
  { key: "U", label: "Unknown", plural: "Unknown" },
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
    { C: [], L: [], R: [], D: [], G: [], U: [] }
  );

  let cardIndex = 0;

  const totalPlayers = players?.length ?? 0;
  const totalSkaters = players?.filter((p) => p.position !== "G" && p.position !== "U").length ?? 0;
  const totalGoalies = players?.filter((p) => p.position === "G").length ?? 0;
  const totalUnknown = players?.filter((p) => p.position === "U").length ?? 0;

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

          <div className="grid grid-cols-5 divide-x divide-slate-100 bg-slate-50 rounded-b-3xl">
            {[
              { label: "Players", value: totalPlayers },
              { label: "Skaters", value: totalSkaters },
              { label: "Goalies", value: totalGoalies },
              { label: "Unknown", value: totalUnknown },
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
          </div>
        </div>
        <div className="space-y-6">
          {POSITION_GROUPS.map((group) => {
            const groupPlayers = grouped[group.key];
            const start = cardIndex;
            cardIndex += groupPlayers.length;
            return (
              <PositionGroup
                key={group.key}
                label={group.plural}
                players={groupPlayers}
                startIndex={start}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default RosterPage;
