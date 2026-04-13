import type { FC } from "react";
import type { PlayerHeaderProps } from "../../types/player";

export const PlayerHeader: FC<PlayerHeaderProps> = ({
  name,
  number,
  team,
  position,
  headshotUrl,
  seasonSummary
}) => {
  return (
    <div className="bg-white rounded-3xl shadow-xl shadow-slate-200/60 overflow-hidden">

      <div className="h-28 bg-gradient-to-r from-blue-700 via-blue-600 to-indigo-700 relative">
        <div
          className="absolute inset-0 opacity-20"
          style={{
            backgroundImage:
              "repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,.15) 10px, rgba(255,255,255,.15) 11px)",
          }}
        />
        <div className="absolute top-3 left-4 text-white/30 font-black text-7xl leading-none select-none">
          {number ?? "N/A"}
        </div>
      </div>

      <div className="px-6 pb-6 text-center relative">
        <div className="relative inline-block -mt-14 mb-3">
          <img
            src={headshotUrl}
            alt={name}
            className="w-28 h-28 rounded-full object-cover border-4 border-white shadow-lg shadow-blue-200/50 bg-slate-100"
          />
        </div>

        <h1 className="text-2xl font-black text-slate-800 tracking-tight">{name}</h1>
        <div className="flex items-center justify-center gap-2 mt-1">
          <span className="text-xs font-semibold text-blue-600 bg-blue-50 px-2.5 py-0.5 rounded-full">
            {team}
          </span>
          <span className="text-xs text-slate-400">·</span>
          <span className="text-xs font-semibold text-slate-500">{position}</span>
        </div>

        <div className="grid gap-2 mt-5 bg-slate-50 rounded-2xl p-3"
          style={{ gridTemplateColumns: `repeat(${seasonSummary.length}, minmax(0, 1fr))` }}
        >
          {seasonSummary.map((s) => (
            <div key={s.label} className="text-center">
              <div className="text-lg font-black text-slate-800">{s.value}</div>
              <div className="text-[10px] font-semibold tracking-wider text-slate-400 uppercase">
                {s.label}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};