export interface DivisionInfo {
  name: string;
  tricodes: string[];
}

export interface ConferenceInfo {
  name: string;
  divisions: DivisionInfo[];
}

export const NHL_CONFERENCES: ConferenceInfo[] = [
  {
    name: "Eastern Conference",
    divisions: [
      {
        name: "Atlantic Division",
        tricodes: ["BOS", "BUF", "DET", "FLA", "MTL", "OTT", "TBL", "TOR"],
      },
      {
        name: "Metropolitan Division",
        tricodes: ["CAR", "CBJ", "NJD", "NYI", "NYR", "PHI", "PIT", "WSH"],
      },
    ],
  },
  {
    name: "Western Conference",
    divisions: [
      {
        name: "Central Division",
        tricodes: ["CHI", "COL", "DAL", "MIN", "NSH", "STL", "WPG", "UTA"],
      },
      {
        name: "Pacific Division",
        tricodes: ["ANA", "CGY", "EDM", "LAK", "SJS", "SEA", "VAN", "VGK"],
      },
    ],
  },
];
