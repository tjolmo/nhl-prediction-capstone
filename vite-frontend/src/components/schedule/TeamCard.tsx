import type { FC } from "react";
import { Link } from "react-router-dom";
import type { Team } from "../../types/teams";

interface TeamCardProps {
    team: Team;
    type: "Away" | "Home";
}

export const TeamCard: FC<TeamCardProps> = ({ team, type }) => {
    return (
        <Link
            to={`/roster/${team.tricode}`}
            className="flex sm:flex-col items-center gap-3 sm:gap-2 sm:w-36 sm:justify-center sm:shrink-0 hover:scale-105 transition-all p-3 rounded-xl hover:bg-slate-50 hover:shadow-md"
        >
            <img
                src={team.logoUrl}
                alt={team.name}
                className="w-14 h-14 sm:w-20 sm:h-20 object-cover drop-shadow-sm"
            />
            <div className="text-center">
                <p className="text-lg sm:text-xl font-black text-slate-500">
                    {team.name}
                </p>
                <p className="text-[10px] font-semibold tracking-wider text-slate-400 uppercase hidden sm:block">
                    {type}
                </p>
            </div>
        </Link>
    );
};
