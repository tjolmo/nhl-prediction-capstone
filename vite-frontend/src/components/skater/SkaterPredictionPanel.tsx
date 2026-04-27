import { useOutletContext } from "react-router-dom";
import type { SkaterData, SkaterStatKey } from "../../types/skater";
import { PlayerPredictionCard } from "../player/PlayerPredictionCard";

const statKeys: SkaterStatKey[] = ["goals", "assists", "points"];

export const SkaterPredictionPanel = () => {
  const { gamePredictions, recentGames } = useOutletContext<SkaterData>();
  if (!gamePredictions || !recentGames) {
    return (
      <div className="bg-white rounded-2xl shadow-lg shadow-slate-200/50 p-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <p className="text-xs font-semibold tracking-widest text-blue-500 uppercase mb-1">
          No game predictions available
        </p>
      </div>
    )
  }
  return (
    <div className="space-y-4">
      <div className="flex gap-3">
        <PlayerPredictionCard
          label="Goals"
          value={gamePredictions.goals}
          icon="🏒"
          color="text-blue-600"
          bgColor="bg-white shadow-lg shadow-slate-200/50"
          subtext={`Prob: ${(gamePredictions.prob_goal * 100).toFixed(0)}%`}
        />
        <PlayerPredictionCard
          label="Assists"
          value={gamePredictions.assists}
          icon="🎯"
          color="text-indigo-600"
          bgColor="bg-white shadow-lg shadow-slate-200/50"
          subtext={`Prob: ${(gamePredictions.prob_assist * 100).toFixed(0)}%`}
        />
        <PlayerPredictionCard
          label="Points"
          value={gamePredictions.points}
          icon="⭐"
          color="text-sky-600"
          bgColor="bg-white shadow-lg shadow-slate-200/50"
          subtext={`Prob: ${(gamePredictions.prob_point * 100).toFixed(0)}%`}
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
                      className={`w-full rounded-sm transition-all duration-500 opacity-80`}
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
