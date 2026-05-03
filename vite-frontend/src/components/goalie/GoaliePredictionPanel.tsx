import { useOutletContext } from "react-router-dom";
import type { GoalieData } from "../../types/goalie";
import { PlayerPredictionCard } from "../player/PlayerPredictionCard";
import { PlayerPropCard } from "../player/PlayerPropCard";

type TrendKey = "goals_against" | "saves" | "save_percentage";

const trendKeys: TrendKey[] = ["goals_against", "saves", "save_percentage"];

const trendLabels: Record<TrendKey, string> = {
  goals_against: "Goals Against",
  saves: "Saves",
  save_percentage: "Save Percentage",
};

export const GoaliePredictionPanel = () => {
  const { gamePredictions, seasonStats, recentGames, playerProps } = useOutletContext<GoalieData>();
  if (!gamePredictions || !seasonStats || !recentGames) {
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
          label="Saves"
          value={gamePredictions.saves}
          icon="🧤"
          color="text-blue-600"
          bgColor="bg-white shadow-lg shadow-slate-200/50"
          subtext={`Season SV%: ${(seasonStats.save_percentage * 100).toFixed(1)}%`}
        />
        <PlayerPredictionCard
          label="GA"
          value={gamePredictions.goals_against}
          icon="🚨"
          color="text-red-500"
          bgColor="bg-white shadow-lg shadow-slate-200/50"
          subtext={`Season GAA: ${seasonStats.gaa.toFixed(2)}`}
        />
      </div>
      {playerProps.length > 0 && (
        <div className={`grid grid-cols-2`}>
          {playerProps.map((prop, index) => (
            <PlayerPropCard key={index} {...prop} />
          ))}
        </div>
      )}

      <div className="bg-white rounded-2xl shadow-lg shadow-slate-200/50 p-5 space-y-4">
        <p className="text-xs font-semibold tracking-widest text-slate-400 uppercase">
          Last 5 Games Trend
        </p>
        {trendKeys.map((stat) => {
          const vals = recentGames.map((g) => g[stat]);
          const max = Math.max(...vals, 1);
          return (
            <div key={stat}>
              <div className="flex justify-between text-xs font-semibold mb-1">
                <span className="text-slate-600">{trendLabels[stat]}</span>
                <span className="text-slate-400">{vals.join(" · ")}</span>
              </div>
              <div className="flex gap-1 h-8 items-end">
                {vals.map((v, i) => (
                  <div key={i} className="flex-1 flex flex-col items-center gap-0.5">
                    <div
                      className="w-full rounded-sm transition-all duration-500 opacity-80"
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
