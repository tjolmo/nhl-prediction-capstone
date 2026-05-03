import type { FC } from "react";
import type { PlayerUpcomingGameProps } from "../../types/player";
import { Link } from "react-router-dom";

export const PlayerUpcomingGame: FC<PlayerUpcomingGameProps> = ({ upcomingGame }) => {
  if (!upcomingGame) {
    return (
      <div className="bg-white rounded-2xl shadow-lg shadow-slate-200/50 p-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <p className="text-xs font-semibold tracking-widest text-blue-500 uppercase mb-1">
          Next Game
        </p>
        <p className="text-xl font-black text-slate-800">No upcoming game</p>
      </div>
    )
  }
  return (
    <div className="bg-white rounded-2xl shadow-lg shadow-slate-200/50 p-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <p className="text-xs font-semibold tracking-widest text-blue-500 uppercase mb-1">
          Next Game
        </p>
        <p className="text-xl font-black text-slate-800">{upcomingGame.home_away === "HOME" ? "vs." : "@ "} <Link to={`/roster/${upcomingGame.opposing_team_tricode}`}>{upcomingGame.opposing_team_tricode}</Link></p>
        <p className="text-sm text-slate-500 mt-0.5">{upcomingGame.venue}</p>
      </div>
      <div className="flex sm:flex-col items-center sm:items-end gap-3 sm:gap-1">
        <span className="text-sm font-bold text-slate-700 bg-blue-50 px-3 py-1.5 rounded-xl">
          {upcomingGame.date}
        </span>
        <span className="text-sm font-bold text-blue-600">
          {/* Convert to local time and format as h:mm A */}
          {new Date(upcomingGame.time).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
        </span>
      </div>
    </div>
  )
};
