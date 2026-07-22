import { useEffect, useState } from "react";
import api from "../services/api";
import {
  FaUsers,
  FaChair,
  FaCheckCircle,
  FaCircle,
  FaLock,
  FaClock,
} from "react-icons/fa";

export default function Dashboard() {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    api
      .get("/dashboard/summary")
      .then((res) => setSummary(res.data))
      .catch(console.error);
  }, []);

  if (!summary) {
    return <h2>Loading...</h2>;
  }

  const cards = [
    {
      title: "Employees",
      value: summary.total_employees,
      icon: <FaUsers className="text-blue-600 text-3xl" />,
      border: "border-blue-500",
    },
    {
      title: "Seats",
      value: summary.total_seats,
      icon: <FaChair className="text-indigo-600 text-3xl" />,
      border: "border-indigo-500",
    },
    {
      title: "Occupied",
      value: summary.occupied_seats,
      icon: <FaCheckCircle className="text-green-600 text-3xl" />,
      border: "border-green-500",
    },
    {
      title: "Available",
      value: summary.available_seats,
      icon: <FaCircle className="text-emerald-500 text-3xl" />,
      border: "border-emerald-500",
    },
    {
      title: "Reserved",
      value: summary.reserved_seats,
      icon: <FaLock className="text-red-500 text-3xl" />,
      border: "border-red-500",
    },
    {
      title: "Pending",
      value: summary.pending_allocation,
      icon: <FaClock className="text-amber-500 text-3xl" />,
      border: "border-amber-500",
    },
  ];

  return (
    <>
      <h2 className="text-3xl font-bold mb-6">Dashboard</h2>

      <div className="grid grid-cols-3 gap-6">
        {cards.map((card) => (
          <div
            key={card.title}
            className={`bg-white rounded-xl shadow-md border-l-4 ${card.border}
    p-6 transition hover:-translate-y-1 hover:shadow-xl`}
          >
            <div className="flex justify-between items-center">
              <div>
                <p className="text-gray-500">{card.title}</p>
                <h2 className="text-4xl font-bold mt-2">{card.value}</h2>
              </div>

              {card.icon}
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
