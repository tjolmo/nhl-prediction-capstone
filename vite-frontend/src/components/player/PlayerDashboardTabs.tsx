import { NavLink } from "react-router-dom";

interface Tab {
    label: string;
    to: string;
    icon: string;
}

interface DashboardTabsProps {
    tabs: Tab[];
}

export const PlayerDashboardTabs: React.FC<DashboardTabsProps> = ({ tabs }) => (
    <div className="flex bg-white rounded-2xl shadow-lg shadow-slate-200/50 p-1.5 gap-1">
        {tabs.map((tab) => (
            <NavLink
                key={tab.to}
                to={tab.to}
                className={({ isActive }) =>
                    `flex-1 py-2.5 text-center text-sm font-bold rounded-xl transition-all ${isActive
                        ? "bg-blue-600 text-white shadow-md shadow-blue-200"
                        : "text-slate-400 hover:text-slate-600"
                    }`
                }
            >
                {tab.icon} {tab.label}
            </NavLink>
        ))}
    </div>
);