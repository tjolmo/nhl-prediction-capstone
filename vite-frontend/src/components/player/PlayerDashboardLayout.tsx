import type { ReactNode } from "react";

interface PlayerDashboardLayoutProps {
    children: ReactNode;
}

export function PlayerDashboardLayout({ children }: PlayerDashboardLayoutProps) {
    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-100 font-sans p-4 sm:p-6 lg:p-10">
            <div className="fixed top-0 right-0 w-96 h-96 bg-blue-400/10 rounded-full blur-3xl pointer-events-none" />
            <div className="fixed bottom-0 left-0 w-64 h-64 bg-indigo-400/10 rounded-full blur-3xl pointer-events-none" />
            <div className="relative max-w-2xl mx-auto space-y-4">
                {children}
            </div>
        </div>
    );
}