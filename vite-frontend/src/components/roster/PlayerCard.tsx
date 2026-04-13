import type { FC } from "react";
import { Link } from "react-router-dom";
import type { PlayerFullData, PlayerCardProps } from "../../types/player";

const getHandednessLabel = (player: PlayerFullData): string => {
  const side = player.shoots_catches === "R" ? "Right" : player.shoots_catches === "L" ? "Left" : "Unknown";
  return player.position === "G" ? `Catches: ${side}` : `Shoots: ${side}`;
};

const POSITION_LABELS: Record<string, string> = {
  C: "Center",
  L: "Left Wing",
  R: "Right Wing",
  D: "Defenseman",
  G: "Goalie",
  U: "Unknown",
};

export const PlayerCard: FC<PlayerCardProps> = ({ player, index }) => {
  const linkTo =
    player.position === "G"
      ? `/goalie/${player.id}`
      : `/player/${player.id}`;

  return (
    <Link
      to={linkTo}
      className="block group"
      style={{ animationDelay: `${index * 60}ms` }}
    >
      <div className="relative overflow-hidden rounded-2xl bg-white shadow-lg shadow-slate-200/50 transition-all duration-300 hover:shadow-xl hover:shadow-blue-100/60 hover:-translate-y-0.5 h-full">
        <div
          className="absolute inset-0 opacity-[0.025]"
          style={{
            backgroundImage:
              "repeating-linear-gradient(45deg, #1e40af, #1e40af 1px, transparent 1px, transparent 12px)",
          }}
        />

        <div className="absolute top-3 left-3 z-10">
          <span className="inline-flex items-center justify-center w-8 h-8 rounded-xl bg-blue-600 text-white text-xs font-black shadow-md shadow-blue-300/40">
            {player.number ?? "N/A"}
          </span>
        </div>

        <div className="absolute top-3 right-3 z-10">
          <span className="inline-block bg-slate-100 text-slate-500 text-[10px] font-black tracking-widest uppercase px-2 py-0.5 rounded-lg">
            {player.position}
          </span>
        </div>

        <div className="relative pt-4 pb-2 flex justify-center bg-gradient-to-b from-blue-50/60 to-transparent">
          <img
            src={player.headshot}
            alt={`${player.first_name} ${player.last_name}`}
            className="w-24 h-24 object-cover rounded-xl"
            onError={(e) => {
              (e.target as HTMLImageElement).src =
                "https://assets.nhle.com/mugs/nhl/default-player.png";
            }}
          />
        </div>

        <div className="relative px-4 pb-4 pt-2 text-center">
          <p className="text-sm font-black text-slate-800 leading-tight">
            {player.first_name}{" "}
            <span className="text-slate-900">{player.last_name}</span>
          </p>
          <p className="text-[10px] font-semibold tracking-wider text-slate-400 uppercase mt-0.5">
            {POSITION_LABELS[player.position]}
          </p>

          <div className="mt-2 pt-2 border-t border-slate-100">
            <span className="text-[10px] font-bold text-blue-600 tracking-wide">
              {getHandednessLabel(player)}
            </span>
          </div>
        </div>

        <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-blue-500 via-indigo-500 to-blue-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      </div>
    </Link>
  );
};
