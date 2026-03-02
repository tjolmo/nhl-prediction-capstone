import type { FC } from "react";
import type { SkaterGameRowProps } from "../types/skater";

export const SkaterGameRow: FC<SkaterGameRowProps> = ({ game_stats, index }) => {
  const isHot = game_stats.points >= 3;
  return (
    <tr
      className="border-b border-slate-100 hover:bg-blue-50/40 transition-colors"
      style={{ animationDelay: `${index * 80}ms` }}
    >
      <td className="py-3 px-4 text-sm text-slate-500 font-medium whitespace-nowrap">
        {game_stats.date}
      </td>
      <td className="py-3 px-4">
        <span className="text-sm font-bold text-slate-700 bg-slate-100 px-2 py-0.5 rounded-md">
          {game_stats.home_away === "HOME" ? "vs" : "@"} {game_stats.opposing_team_tricode}
        </span>
      </td>
      <td className="py-3 px-4 text-center">
        <span className={`text-sm font-bold ${game_stats.goals > 0 ? "text-blue-600" : "text-slate-300"}`}>
          {game_stats.goals}
        </span>
      </td>
      <td className="py-3 px-4 text-center">
        <span className={`text-sm font-bold ${game_stats.assists > 0 ? "text-indigo-600" : "text-slate-300"}`}>
          {game_stats.assists}
        </span>
      </td>
      <td className="py-3 px-4 text-center">
        <span
          className={`inline-flex items-center justify-center w-7 h-7 rounded-full text-sm font-black ${
            isHot
              ? "bg-blue-600 text-white shadow-sm shadow-blue-200"
              : "text-slate-600 font-bold"
          }`}
        >
          {game_stats.points}
        </span>
      </td>
    </tr>
  );
};