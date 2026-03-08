import type { FC } from "react";
import type { PlayerPredictionCardProps } from "../../types/player";

export const SkaterPredictionCard: FC<PlayerPredictionCardProps> = ({
  label,
  value,
  icon,
  color,
  bgColor,
  subtext,
}) => (
  <div
    className={`relative overflow-hidden rounded-2xl p-5 ${bgColor} flex-1`}
    style={{ minWidth: 0 }}
  >
    <div className="flex items-start justify-between mb-1">
      <span className="text-xs font-semibold tracking-widest uppercase text-slate-400">
        {label}
      </span>
      <span className="text-lg">{icon}</span>
    </div>
    <div className={`text-5xl font-black mt-1 ${color} leading-none`}>
      {value}
    </div>
    <div className="text-xs text-slate-400 mt-2 font-medium">{subtext}</div>
    <div
      className={`absolute -bottom-4 -right-4 w-20 h-20 rounded-full opacity-10 ${color.replace(
        "text-",
        "bg-"
      )}`}
    />
  </div>
);