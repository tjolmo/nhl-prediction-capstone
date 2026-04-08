import type { FC } from "react";
import { useNavigate } from "react-router-dom";

interface ErrorPageProps {
  message?: string;
}

const ErrorPage: FC<ErrorPageProps> = ({ message }) => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-100 font-sans flex items-center justify-center p-4">
      <div className="fixed top-0 right-0 w-96 h-96 bg-red-400/10 rounded-full blur-3xl pointer-events-none" />
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
              Something Went Wrong
            </h1>
            <p className="text-blue-200 text-xs font-semibold mt-0.5 tracking-widest uppercase">
              Error
            </p>
          </div>
        </div>

        <div className="flex flex-col items-center justify-center py-10 px-6 gap-5">
          <div className="w-16 h-16 rounded-full bg-red-50 border-2 border-red-100 flex items-center justify-center shadow-inner">
            <span className="text-3xl select-none" role="img" aria-label="Error">
              ⚠️
            </span>
          </div>

          <div className="text-center space-y-1">
            <p className="text-slate-700 font-semibold text-sm">
              {message ?? "We couldn't load this page."}
            </p>
            <p className="text-slate-400 text-xs">
              Please check your connection and try again.
            </p>
          </div>

          <div className="flex gap-3 w-full pt-1">
            <button
              onClick={() => navigate(-1)}
              className="flex-1 py-2 rounded-xl border border-slate-200 text-slate-600 text-sm font-semibold hover:bg-slate-50 transition-colors"
            >
              ← Go Back
            </button>
            <button
              onClick={() => navigate("/")}
              className="flex-1 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-sm font-semibold hover:from-blue-700 hover:to-indigo-700 transition-all shadow"
            >
              Home
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ErrorPage;
