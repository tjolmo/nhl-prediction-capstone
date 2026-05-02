import { useOutletContext } from "react-router-dom";
import type { GoalieData } from "../../types/goalie";
import { GoalieGameRow } from "./GoalieGameRow";

export const GoalieRecentGames = () => {
  const { recentGames } = useOutletContext<GoalieData>();

  return (
    <div className="bg-white rounded-2xl shadow-lg shadow-slate-200/50 overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-100">
        <p className="text-xs font-semibold tracking-widest text-slate-400 uppercase">
          Last 5 Games
        </p>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[400px]">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-100">
              {(["Date", "OPP", "SV", "SV%", "GA"] as const).map((h) => (
                <th
                  key={h}
                  className={`py-3 px-4 text-[10px] font-black tracking-widest text-slate-400 uppercase ${["SV", "GA", "SV%"].includes(h) ? "text-center" : "text-left"
                    }`}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {recentGames.map((game, i) => (
              <GoalieGameRow key={i} game_stats={game} index={i} />
            ))}
          </tbody>
          <tfoot>
            <tr className="bg-blue-50/50 border-t-2 border-slate-100">
              <td
                className="py-3 px-4 text-xs font-black text-slate-500 uppercase tracking-wider"
                colSpan={2}
              >
                Average
              </td>
              <td className="py-3 px-4 text-center text-sm font-black text-blue-700">
                {recentGames.length > 0 ? (recentGames.reduce((s, g) => s + g.saves, 0) / recentGames.length).toFixed(1) : "0.0"}
              </td><td className="py-3 px-4 text-center text-sm font-black text-slate-600">
                {recentGames.length > 0 ? (recentGames.reduce((s, g) => s + g.save_percentage, 0) / recentGames.length).toFixed(3) + "" : "0.000"}
              </td>
              <td className="py-3 px-4 text-center text-sm font-black text-red-500">
                {recentGames.length > 0 ? (recentGames.reduce((s, g) => s + g.goals_against, 0) / recentGames.length).toFixed(1) : "0.0"}
              </td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  );
};
