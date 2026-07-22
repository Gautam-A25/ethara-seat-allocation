import { useState, useEffect, useCallback } from "react";
import { FaSearch } from "react-icons/fa";
import api from "../services/api";
import Pagination from "../components/Pagination";
import StatusBadge from "../components/StatusBadge";

const LIMIT = 25;

export default function Employees() {
  const [employees, setEmployees] = useState([]);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(true);

  const loadEmployees = useCallback(async () => {
    setLoading(true);

    try {
      const res = await api.get("/employees", {
        params: {
          skip: page * LIMIT,
          limit: LIMIT,
        },
      });

      setEmployees(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [page]);

  useEffect(() => {
    loadEmployees();
  }, [loadEmployees]);

  const filteredEmployees = employees.filter((emp) =>
    `${emp.employee_code} ${emp.name} ${emp.email} ${emp.department} ${emp.role}`
      .toLowerCase()
      .includes(search.toLowerCase()),
  );

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-3xl font-bold text-slate-800">Employees</h2>
          <p className="text-gray-500 mt-1">View and manage all employees.</p>
        </div>

        <div className="relative">
          <FaSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />

          <input
            type="text"
            placeholder="Search employees..."
            className="w-80 rounded-lg border border-gray-300 pl-10 pr-4 py-2 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      <div className="overflow-hidden rounded-xl bg-white shadow-md">
        <table className="w-full">
          <thead className="bg-slate-900 text-white">
            <tr>
              <th className="p-4 text-left">Employee Code</th>
              <th className="p-4 text-left">Name</th>
              <th className="p-4 text-left">Department</th>
              <th className="p-4 text-left">Role</th>
              <th className="p-4 text-left">Status</th>
            </tr>
          </thead>

          <tbody>
            {loading ? (
              <tr>
                <td colSpan="5" className="py-10 text-center text-gray-500">
                  Loading employees...
                </td>
              </tr>
            ) : filteredEmployees.length === 0 ? (
              <tr>
                <td colSpan="5" className="py-10 text-center text-gray-500">
                  No employees found.
                </td>
              </tr>
            ) : (
              filteredEmployees.map((emp, index) => (
                <tr
                  key={emp.id}
                  className={`border-b transition hover:bg-slate-100 ${
                    index % 2 === 0 ? "bg-white" : "bg-slate-50"
                  }`}
                >
                  <td className="p-4 font-medium">{emp.employee_code}</td>
                  <td className="p-4">{emp.name}</td>
                  <td className="p-4">{emp.department}</td>
                  <td className="p-4">{emp.role}</td>
                  <td className="p-4">
                    <StatusBadge status={emp.status} />
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <Pagination
        page={page}
        hasNext={employees.length === LIMIT}
        onPrevious={() => setPage((prev) => Math.max(prev - 1, 0))}
        onNext={() => setPage((prev) => prev + 1)}
      />
    </div>
  );
}
