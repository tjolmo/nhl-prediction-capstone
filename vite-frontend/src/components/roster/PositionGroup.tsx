import type { FC } from "react";
import type { PositionGroupProps } from "../../types/player";
import { PlayerCard } from "./PlayerCard";

export const PositionGroup: FC<PositionGroupProps> = ({
  label,
  players,
  startIndex,
}) => {
  if (players.length === 0) return null;

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2">
          <div className="w-1 h-5 rounded-full bg-blue-600" />
          <h2 className="text-sm font-black text-slate-700 tracking-widest uppercase">
            {label}
          </h2>
          <span className="inline-flex items-center justify-center w-5 h-5 rounded-lg bg-blue-50 text-blue-600 text-[10px] font-black">
            {players.length}
          </span>
        </div>
        <div className="flex-1 h-px bg-slate-200" />
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        {players.map((player, i) => (
          <PlayerCard
            key={player.id}
            player={player}
            index={startIndex + i}
          />
        ))}
      </div>
    </div>
  );
};
