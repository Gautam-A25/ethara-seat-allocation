import { NavLink } from "react-router-dom";
import {
  FaChartBar,
  FaUsers,
  FaChair,
  FaProjectDiagram,
  FaRobot,
} from "react-icons/fa";

const menu = [
  {
    name: "Dashboard",
    path: "/dashboard",
    icon: <FaChartBar />,
  },
  {
    name: "Employees",
    path: "/employees",
    icon: <FaUsers />,
  },
  {
    name: "Seats",
    path: "/seats",
    icon: <FaChair />,
  },
  {
    name: "Projects",
    path: "/projects",
    icon: <FaProjectDiagram />,
  },
  {
    name: "AI Assistant",
    path: "/ai",
    icon: <FaRobot />,
  },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 text-white flex flex-col shadow-2xl">
      {/* Logo */}
      <div className="p-6 border-b border-slate-700">
        <h1 className="text-3xl font-extrabold tracking-wider text-white">
          ETHARA
        </h1>

        <p className="text-sm text-slate-400 mt-1">Seat Allocation System</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 mt-4 px-3">
        {menu.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-4 py-3 mb-2 transition-all duration-200 ${
                isActive
                  ? "bg-blue-600 shadow-lg font-semibold"
                  : "hover:bg-slate-800 hover:translate-x-1"
              }`
            }
          >
            <span className="text-lg">{item.icon}</span>
            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="border-t border-slate-700 p-4 text-center text-xs text-slate-500">
        © 2026 Ethara
      </div>
    </aside>
  );
}
