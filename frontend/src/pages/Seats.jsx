import { useState, useEffect, useCallback } from "react";
import { FaSearch } from "react-icons/fa";
import api from "../services/api";
import Pagination from "../components/Pagination";
import StatusBadge from "../components/StatusBadge";

const LIMIT = 25;

export default function Seats() {
  const [seats, setSeats] = useState([]);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(true);

  const loadSeats = useCallback(async () => {
    setLoading(true);

    try {
      const res = await api.get("/seats", {
        params: {
          skip: page * LIMIT,
          limit: LIMIT,
        },
      });

      setSeats(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [page]);

  useEffect(() => {
    loadSeats();
  }, [loadSeats]);

  const filteredSeats = seats.filter((seat) =>
    `${seat.seat_number} ${seat.zone} ${seat.bay} ${seat.floor}`
      .toLowerCase()
      .includes(search.toLowerCase()),
  );

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-3xl font-bold text-slate-800">Seats</h2>
          <p className="text-gray-500 mt-1">
            View and manage all available seats.
          </p>
        </div>

        <div className="relative">
          <FaSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />

          <input
            type="text"
            placeholder="Search seats..."
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
              <th className="p-4 text-left">Seat Number</th>
              <th className="p-4 text-left">Floor</th>
              <th className="p-4 text-left">Zone</th>
              <th className="p-4 text-left">Bay</th>
              <th className="p-4 text-left">Status</th>
            </tr>
          </thead>

          <tbody>
            {loading ? (
              <tr>
                <td colSpan="5" className="py-10 text-center text-gray-500">
                  Loading seats...
                </td>
              </tr>
            ) : filteredSeats.length === 0 ? (
              <tr>
                <td colSpan="5" className="py-10 text-center text-gray-500">
                  No seats found.
                </td>
              </tr>
            ) : (
              filteredSeats.map((seat, index) => (
                <tr
                  key={seat.id}
                  className={`border-b transition hover:bg-slate-100 ${
                    index % 2 === 0 ? "bg-white" : "bg-slate-50"
                  }`}
                >
                  <td className="p-4 font-medium">{seat.seat_number}</td>
                  <td className="p-4">Floor {seat.floor}</td>
                  <td className="p-4">Zone {seat.zone}</td>
                  <td className="p-4">{seat.bay}</td>
                  <td className="p-4">
                    <StatusBadge status={seat.status} />
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <Pagination
        page={page}
        hasNext={seats.length === LIMIT}
        onPrevious={() => setPage((prev) => Math.max(prev - 1, 0))}
        onNext={() => setPage((prev) => prev + 1)}
      />
    </div>
  );
}
