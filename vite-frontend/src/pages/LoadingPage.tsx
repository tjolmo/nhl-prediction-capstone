import type { FC } from "react";

const LoadingPage: FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-100 font-sans flex items-center justify-center p-4">
      <div className="fixed top-0 right-0 w-96 h-96 bg-blue-400/10 rounded-full blur-3xl pointer-events-none" />
      <div className="fixed bottom-0 left-0 w-64 h-64 bg-indigo-400/10 rounded-full blur-3xl pointer-events-none" />

      <div className="relative bg-white rounded-3xl shadow-xl shadow-slate-200/60 overflow-hidden w-full max-w-sm">
        <div className="h-20 bg-gradient-to-r from-blue-700 via-blue-600 to-indigo-700 relative">
          <div
            className="absolute inset-0 opacity-20"
            style={{
              backgroundImage:
                "repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,.15) 10px, rgba(255,255,255,.15) 11px)",
            }}
          />
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <h1 className="text-white font-black text-2xl tracking-tight drop-shadow">
              Loading
            </h1>
            <p className="text-blue-200 text-xs font-semibold mt-0.5 tracking-widest uppercase">
              Please wait…
            </p>
          </div>
        </div>

        <div className="flex flex-col items-center justify-center py-10 gap-5">
          <div className="relative w-16 h-16">
            <div className="absolute inset-0 rounded-full border-4 border-slate-100" />
            <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-blue-600 animate-spin" />
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-4 h-4 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 shadow-md animate-pulse" />
            </div>
          </div>

          <div className="text-center space-y-1">
            <p className="text-slate-700 font-semibold text-sm">Fetching data…</p>
            <p className="text-slate-400 text-xs">This should only take a moment</p>
          </div>

          <div className="flex gap-1.5">
            {[0, 1, 2].map((i) => (
              <div
                key={i}
                className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-bounce"
                style={{ animationDelay: `${i * 0.15}s` }}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingPage;
