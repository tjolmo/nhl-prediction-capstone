import type { FC } from "react";
import { useTeams } from "../hooks/useTeams";
import { NHL_CONFERENCES } from "../data/nhlDivisions";
import { ConferenceSection } from "../components/teams/ConferenceSection";
import type { Team } from "../types/teams";
import ErrorPage from "./ErrorPage";
import LoadingPage from "./LoadingPage";

export const TeamsPage: FC = () => {
  const { data: teams, loading, error } = useTeams();

  if (error) return <ErrorPage message="Error loading teams." />;
  if (loading) return <LoadingPage />;

  const teamsByTricode = new Map<string, Team>(
    (teams ?? []).map((t) => [t.tricode, t])
  );

  const totalTeams = teams?.length ?? 0;

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
                NHL Teams
              </h1>
              <p className="text-blue-200 text-xs font-semibold mt-0.5 tracking-widest uppercase">
                {loading ? "Loading…" : `${totalTeams} Teams`}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 divide-x divide-slate-100 bg-slate-50 rounded-b-3xl">
            {[
              { label: "Conferences", value: 2 },
              { label: "Divisions", value: 4 },
            ].map((s) => (
              <div key={s.label} className="py-3 text-center">
                <p className="text-lg font-black text-slate-800">{s.value}</p>
                <p className="text-[10px] font-semibold tracking-wider text-slate-400 uppercase">
                  {s.label}
                </p>
              </div>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="space-y-10">
            {[0, 1].map((ci) => (
              <div key={ci} className="space-y-6">
                <div className="flex items-center gap-4">
                  <div className="h-0.5 w-5 bg-blue-600/30 rounded-full" />
                  <div className="h-4 w-48 bg-slate-200 rounded-lg animate-pulse" />
                  <div className="flex-1 h-0.5 bg-slate-200 rounded-full" />
                </div>
                {[0, 1].map((di) => (
                  <div key={di} className="space-y-3">
                    <div className="flex items-center gap-3">
                      <div className="h-3 w-32 bg-slate-200 rounded-lg animate-pulse" />
                      <div className="flex-1 h-px bg-slate-200" />
                    </div>
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                      {Array.from({ length: 8 }).map((_, i) => (
                        <div
                          key={i}
                          className="bg-white rounded-2xl shadow-lg shadow-slate-200/50 h-36 animate-pulse"
                        />
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ))}
          </div>
        ) : (
          <div className="space-y-10">
            {NHL_CONFERENCES.map((conference) => (
              <ConferenceSection
                key={conference.name}
                conference={conference}
                teamsByTricode={teamsByTricode}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TeamsPage;
