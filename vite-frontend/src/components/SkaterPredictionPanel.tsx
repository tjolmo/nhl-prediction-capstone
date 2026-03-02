import { useOutletContext } from "react-router-dom";
import type { SkaterData, SkaterStatKey } from "../types/skater";
import { PlayerPredictionCard } from "./PlayerPredictionCard";

const statKeys: SkaterStatKey[] = ["goals", "assists", "points"];
const trendColors: Record<SkaterStatKey, string> = {
  goals: "bg-blue-500",
  assists: "bg-indigo-500",
  points: "bg-sky-500",
};

export const SkaterPredictionPanel = () => {
  const { gamePredictions, seasonStats, recentGames } = useOutletContext<SkaterData>();

  return (
    <div className="space-y-4">
      <div className="flex gap-3">
        <PlayerPredictionCard
          label="Goals"
          value={gamePredictions.goals}
          icon="🏒"
          color="text-blue-600"
          bgColor="bg-white shadow-lg shadow-slate-200/50"
          subtext={`Season avg: ${(seasonStats.goals / seasonStats.games).toFixed(2)}/gm`}
        />
        <PlayerPredictionCard
          label="Assists"
          value={gamePredictions.assists}
          icon="🎯"
          color="text-indigo-600"
          bgColor="bg-white shadow-lg shadow-slate-200/50"
          subtext={`Season avg: ${(seasonStats.assists / seasonStats.games).toFixed(2)}/gm`}
        />
        <PlayerPredictionCard
          label="Points"
          value={gamePredictions.points}
          icon="⭐"
          color="text-sky-600"
          bgColor="bg-white shadow-lg shadow-slate-200/50"
          subtext={
            <span className="text-blue-200">
              {`Season avg: ${(seasonStats.points / seasonStats.games).toFixed(2)}/gm`}
            </span>
          }
        />
      </div>

      <div className="bg-white rounded-2xl shadow-lg shadow-slate-200/50 p-5 space-y-4">
        <p className="text-xs font-semibold tracking-widest text-slate-400 uppercase">
          Last 5 Games Trend
        </p>
        {statKeys.map((stat) => {
          const vals = recentGames.map((g) => g[stat]);
          const max = Math.max(...vals, 1);
          return (
            <div key={stat}>
              <div className="flex justify-between text-xs font-semibold mb-1">
                <span className="capitalize text-slate-600">{stat}</span>
                <span className="text-slate-400">{vals.join(" · ")}</span>
              </div>
              <div className="flex gap-1 h-8 items-end">
                {vals.map((v, i) => (
                  <div key={i} className="flex-1 flex flex-col items-center gap-0.5">
                    <div
                      className={`w-full rounded-sm ${trendColors[stat]} transition-all duration-500 opacity-80`}
                      style={{
                        height: `${Math.max((v / max) * 100, 10)}%`,
                        animationDelay: `${i * 100}ms`,
                      }}
                    />
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
