"use client";
import React, { useEffect, useState } from "react";
import { fetchHealthHistory } from "@/lib/health";

export default function HealthHistory() {
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHealthHistory()
      .then(setLogs)
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading health history...</p>;

  if (logs.length === 0) return <p>No health records found.</p>;

  return (
    <div className="space-y-4 mt-6">
      <h2 className="text-xl font-semibold">Health History</h2>
      {logs.map((log) => (
        <div key={log.id} className="border rounded p-4 shadow">
          <div className="text-xs text-gray-500">{new Date(log.timestamp).toLocaleString()}</div>
          <p className="text-sm italic mt-1">{log.input}</p>
          <p className="mt-2 text-sm"><strong>Status:</strong> {log.status}</p>
          <ul className="list-disc list-inside text-sm mt-2">
            {log.recommendations.map((r: string, i: number) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
