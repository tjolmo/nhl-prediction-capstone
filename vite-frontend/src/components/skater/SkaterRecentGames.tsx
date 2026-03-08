import { useOutletContext } from "react-router-dom";
import type { SkaterData, SkaterStatKey } from "../../types/skater";
import { SkaterGameRow } from "./SkaterGameRow";

const statKeys: SkaterStatKey[] = ["goals", "assists", "points"];

export const SkaterRecentGames = () => {
  const { recentGames } = useOutletContext<SkaterData>();

  return (
    <div className="bg-white rounded-2xl shadow-lg shadow-slate-200/50 overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-100">
        <p className="text-xs font-semibold tracking-widest text-slate-400 uppercase">
          Last 5 Games
        </p>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[360px]">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-100">
              {(["Date", "OPP", "G", "A", "PTS"] as const).map((h) => (
                <th
                  key={h}
                  className={`py-3 px-4 text-[10px] font-black tracking-widest text-slate-400 uppercase ${["G", "A", "PTS"].includes(h) ? "text-center" : "text-left"
                    }`}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {recentGames.map((game, i) => (
              <SkaterGameRow key={i} game_stats={game} index={i} />
            ))}
          </tbody>
          <tfoot>
            <tr className="bg-blue-50/50 border-t-2 border-slate-100">
              <td
                className="py-3 px-4 text-xs font-black text-slate-500 uppercase tracking-wider"
                colSpan={2}
              >
                Total
              </td>
              {statKeys.map((stat) => (
                <td
                  key={stat}
                  className="py-3 px-4 text-center text-sm font-black text-blue-700"
                >
                  {recentGames.reduce((s, g) => s + g[stat], 0)}
                </td>
              ))}
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  );
};
