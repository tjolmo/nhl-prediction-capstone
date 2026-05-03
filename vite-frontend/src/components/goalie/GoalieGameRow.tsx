import type { FC } from "react";
import type { GoalieGameRowProps } from "../../types/goalie";
import { Link } from "react-router-dom";

export const GoalieGameRow: FC<GoalieGameRowProps> = ({ game_stats, index }) => {
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
          <Link to={`/roster/${game_stats.opposing_team_tricode}`}>
            {game_stats.home_away === "HOME" ? "vs " : "@ "}{game_stats.opposing_team_tricode}
          </Link>
        </span>
      </td>
      <td className="py-3 px-4 text-center">
        <span
          className={`inline-flex items-center justify-center w-8 h-7 rounded-full text-sm font-black ${game_stats.saves >= 30 ? "bg-emerald-500 text-white" : "bg-slate-100 text-slate-600"
            }`}
        >
          {game_stats.saves}
        </span>
      </td>
      <td className="py-3 px-4 text-center">
        <span className="text-sm font-bold text-slate-600">
          {game_stats.save_percentage.toFixed(3)}
        </span>
      </td>
      <td className="py-3 px-4 text-center">
        <span
          className={`text-sm font-bold ${game_stats.goals_against === 0 ? "text-emerald-600" : game_stats.goals_against >= 3 ? "text-red-500" : "text-slate-500"
            }`}
        >
          {game_stats.goals_against}
        </span>
      </td>
    </tr>
  );
};
