import { useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useSearch } from "../hooks/useSearch";

export default function SearchBar() {
    const { query, setQuery, results, hasResults, loading } = useSearch(300);
    const navigate = useNavigate();
    const containerRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLInputElement>(null);

    const showDropdown = query.trim().length > 0 && (hasResults || loading);

    useEffect(() => {
        const handleClick = (e: MouseEvent) => {
            if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
                setQuery("");
            }
        };
        document.addEventListener("mousedown", handleClick);
        return () => document.removeEventListener("mousedown", handleClick);
    }, [setQuery]);

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter" && query.trim()) {
            navigate(`/search?q=${encodeURIComponent(query.trim())}`);
            setQuery("");
            inputRef.current?.blur();
        }
    };

    const handlePlayerClick = (id: number, position: string | null) => {
        const route = position === "G" ? `/goalie/${id}` : `/player/${id}`;
        navigate(route);
        setQuery("");
    };

    const handleTeamClick = (tricode: string) => {
        navigate(`/roster/${tricode}`);
        setQuery("");
    };

    return (
        <div ref={containerRef} className="relative ml-auto">
            <div className="relative">
                <svg
                    className="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth={2}
                    viewBox="0 0 24 24"
                >
                    <circle cx="11" cy="11" r="8" />
                    <path d="m21 21-4.35-4.35" strokeLinecap="round" />
                </svg>
                <input
                    ref={inputRef}
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Search players/teams…"
                    className="w-48 pl-8 pr-3 py-1.5 rounded-xl bg-slate-100 text-sm text-slate-700
                               placeholder:text-slate-400 border border-transparent
                               focus:outline-none focus:border-blue-400 focus:bg-white focus:shadow-sm
                               transition-all"
                />
                {loading && (
                    <div className="absolute right-2.5 top-1/2 -translate-y-1/2 w-4 h-4 border-2 border-slate-300 border-t-blue-500 rounded-full animate-spin" />
                )}
            </div>

            {showDropdown && (
                <div className="absolute top-full right-0 mt-2 w-72 bg-white rounded-2xl shadow-xl shadow-slate-200/80 border border-slate-100 overflow-hidden z-50">
                    {!hasResults && loading ? (
                        <div className="px-4 py-6 text-center text-sm text-slate-400">Searching…</div>
                    ) : (
                        <>
                            {results.players.length > 0 && (
                                <div>
                                    <div className="px-3 pt-2.5 pb-1 text-[10px] font-semibold uppercase tracking-wider text-slate-400">
                                        Players
                                    </div>
                                    {results.players.map((player) => (
                                        <button
                                            key={player.id}
                                            onClick={() => handlePlayerClick(player.id, player.position)}
                                            className="w-full flex items-center gap-3 px-3 py-2.5 hover:bg-blue-50/60 transition-colors text-left cursor-pointer"
                                        >
                                            <img
                                                src={player.headshot || ""}
                                                alt={`${player.first_name} ${player.last_name}`}
                                                className="w-10 h-10 rounded-full bg-slate-100 object-cover flex-shrink-0"
                                                onError={(e) => {
                                                    (e.target as HTMLImageElement).src =
                                                        "https://assets.nhle.com/mugs/actionshot/1024x1024/placeholder.png";
                                                }}
                                            />
                                            <div className="min-w-0 flex-1">
                                                <p className="text-sm font-semibold text-slate-800 truncate">
                                                    {player.first_name} {player.last_name}
                                                </p>
                                                <p className="text-xs text-slate-400 font-medium">
                                                    {player.current_team_tri_code ?? "No Team"}{" "}
                                                    <span className="text-slate-300">·</span>{" "}
                                                    {player.position ?? ""}
                                                </p>
                                            </div>
                                        </button>
                                    ))}
                                </div>
                            )}
                            {results.players.length > 0 && results.teams.length > 0 && (
                                <div className="border-t border-slate-100" />
                            )}
                            {results.teams.length > 0 && (
                                <div>
                                    <div className="px-3 pt-2.5 pb-1 text-[10px] font-semibold uppercase tracking-wider text-slate-400">
                                        Teams
                                    </div>
                                    {results.teams.map((team) => (
                                        <button
                                            key={team.tricode}
                                            onClick={() => handleTeamClick(team.tricode)}
                                            className="w-full flex items-center gap-3 px-3 py-2.5 hover:bg-blue-50/60 transition-colors text-left cursor-pointer"
                                        >
                                            <img
                                                src={team.logoUrl || ""}
                                                alt={team.name}
                                                className="w-10 h-10 rounded-lg bg-slate-100 object-contain flex-shrink-0 p-1"
                                                onError={(e) => {
                                                    (e.target as HTMLImageElement).style.display = "none";
                                                }}
                                            />
                                            <div className="min-w-0 flex-1">
                                                <p className="text-sm font-semibold text-slate-800 truncate">
                                                    {team.name}
                                                </p>
                                                <p className="text-xs text-slate-400 font-medium">
                                                    {team.tricode}
                                                </p>
                                            </div>
                                        </button>
                                    ))}
                                </div>
                            )}
                        </>
                    )}

                    {hasResults && (
                        <div className="border-t border-slate-100 px-4 py-2 text-[11px] text-slate-400 text-center">
                            Press <kbd className="px-1 py-0.5 bg-slate-100 rounded text-[10px] font-mono">Enter</kbd> for full results
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
