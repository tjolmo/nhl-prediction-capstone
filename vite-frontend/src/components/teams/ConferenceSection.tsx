import type { FC } from "react";
import type { Team } from "../../types/teams";
import type { ConferenceInfo } from "../../data/nhlDivisions";
import { DivisionSection } from "./DivisionSection";

interface ConferenceSectionProps {
  conference: ConferenceInfo;
  teamsByTricode: Map<string, Team>;
}

export const ConferenceSection: FC<ConferenceSectionProps> = ({
  conference,
  teamsByTricode,
}) => {
  return (
    <div className="space-y-6">
      {/* Conference header */}
      <div className="flex items-center gap-4">
        <div className="h-0.5 w-5 bg-blue-600 rounded-full" />
        <h2 className="text-base font-black text-slate-700 tracking-wide">
          {conference.name}
        </h2>
        <div className="flex-1 h-0.5 bg-blue-600/20 rounded-full" />
      </div>

      <div className="space-y-6">
        {conference.divisions.map((division) => {
          const teams = division.tricodes
            .map((tc) => teamsByTricode.get(tc))
            .filter((t): t is Team => t !== undefined);

          return (
            <DivisionSection
              key={division.name}
              division={division}
              teams={teams}
            />
          );
        })}
      </div>
    </div>
  );
};
