export default function Topbar() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200 px-8 py-5 flex justify-between items-center">
      <div>
        <h1 className="text-3xl font-bold text-slate-800">
          Ethara Seat Allocation System
        </h1>

        <p className="text-sm text-gray-500 mt-1">
          Workspace & Employee Management Dashboard
        </p>
      </div>

      <div className="text-right">
        <p className="text-sm text-gray-500">Welcome</p>

        <p className="font-semibold text-slate-800">Admin Dashboard</p>
      </div>
    </header>
  );
}
