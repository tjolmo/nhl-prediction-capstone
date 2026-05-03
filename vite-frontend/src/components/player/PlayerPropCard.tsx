import type { FC } from "react";
import type { PlayerPropData } from "../../types/player";

const formatOdds = (odds: number): string =>
    odds > 0 ? `+${odds}` : `${odds}`;

const formatPropType = (prop_type: string): string => {
    const map: Record<string, string> = {
        "player_goals": "Goals",
        "player_assists": "Assists",
        "player_points": "Points",
        "player_total_saves": "Saves",
    };
    return map[prop_type] || prop_type;
}

export const PlayerPropCard: FC<PlayerPropData> = ({ over_under, line, odds, prop_type }) => {
    const isOver = over_under.toUpperCase() === "OVER";

    const directionClasses = isOver
        ? "bg-emerald-50 text-emerald-700"
        : "bg-rose-50 text-rose-700";

    return (
        <div className="relative overflow-hidden rounded-2xl bg-white shadow-lg shadow-slate-200/50 hover:shadow-xl hover:-translate-y-0.5 transition p-5">
            <div className="text-xs font-semibold tracking-widest uppercase text-slate-400 mb-3">
                {formatPropType(prop_type)}
            </div>

            <div className="flex items-center justify-between gap-4">
                <div className="flex items-center gap-2 min-w-0">
                    <span
                        className={`inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-semibold ${directionClasses}`}
                    >
                        <span aria-hidden="true">{isOver ? "▲" : "▼"}</span>
                        {isOver ? "OVER" : "UNDER"}
                    </span>
                    <span className="text-2xl font-black text-slate-800 leading-none">
                        {line}
                    </span>
                </div>

                <span className="inline-flex items-center rounded-lg bg-blue-50 px-3 py-1.5 text-sm font-bold text-blue-700 tabular-nums">
                    {formatOdds(odds)}
                </span>
            </div>
        </div>
    );
};
