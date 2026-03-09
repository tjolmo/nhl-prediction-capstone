import type { FC } from "react";
import type { Team } from "../../types/teams";
import type { DivisionInfo } from "../../data/nhlDivisions";
import { TeamCard } from "../schedule/TeamCard";

interface DivisionSectionProps {
  division: DivisionInfo;
  teams: Team[];
}

export const DivisionSection: FC<DivisionSectionProps> = ({ division, teams }) => {
  if (teams.length === 0) return null;

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-3">
        <h3 className="text-xs font-black tracking-widest text-slate-400 uppercase whitespace-nowrap">
          {division.name}
        </h3>
        <div className="flex-1 h-px bg-slate-200" />
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {teams.map((team) => (
          <div
            key={team.tricode}
            className="bg-white rounded-2xl shadow-lg shadow-slate-200/50 flex items-center justify-center hover:shadow-xl hover:shadow-blue-100/60 transition-all duration-300 hover:-translate-y-0.5 p-2"
          >
            <TeamCard team={team} />
          </div>
        ))}
      </div>
    </div>
  );
};
