"use client";

import { useEffect, useState } from "react";
import FinanceForm from "@/components/FinanceForm";

if (!process.env.NEXT_PUBLIC_API_URL) {
  throw new Error("API base URL is not defined!");
}
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;


export default function FinancePage() {
  const [entries, setEntries] = useState<any[]>([]);

  useEffect(() => {
    async function fetchEntries() {
      const res = await fetch(`${API_BASE_URL}/api/finance/all`);
      const data = await res.json();
      setEntries(data);
    }
    fetchEntries();
  }, []);

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">💸 Finance Tracker</h1>
      <FinanceForm onNew={(entry) => setEntries((prev) => [entry, ...prev])} />
      <ul className="mt-6 space-y-2">
        {entries.map((entry) => (
          <li key={entry.id} className="p-3 bg-gray-100 rounded flex justify-between">
            <div>
              <span className="block font-medium capitalize">{entry.type}</span>
              <span className="text-xs text-gray-500">{entry.category}</span>
            </div>
            <span className={`${entry.type === "income" ? "text-green-600" : "text-red-600"}`}>
              ₹{entry.amount}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
