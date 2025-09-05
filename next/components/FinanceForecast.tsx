"use client";
import { useEffect, useState } from "react";

if (!process.env.NEXT_PUBLIC_API_URL) {
  throw new Error("API base URL is not defined!");
}
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export default function FinanceForecast() {
  const [forecast, setForecast] = useState<any>(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/finance/forecast`)
      .then((res) => res.json())
      .then(setForecast);
  }, []);

  if (!forecast) return <p>Loading forecast...</p>;

  return (
    <div className="p-4">
      <h2 className="font-bold text-xl">Financial Forecast</h2>
      <ul className="mt-2">
        {forecast.labels.map((month: string, i: number) => (
          <li key={month}>
            {month}: Savings ₹{forecast.predicted_savings[i]} & Expenses ₹{forecast.predicted_expenses[i]}
          </li>
        ))}
      </ul>
    </div>
  );
}
