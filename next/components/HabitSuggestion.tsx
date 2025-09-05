// components/HabitSuggestion.tsx
"use client";

import React, { useEffect, useState } from "react";

if (!process.env.NEXT_PUBLIC_API_URL) {
  throw new Error("API base URL is not defined!");
}
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export default function HabitSuggestion() {
  const [habits, setHabits] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchSuggestions() {
      try {
        const res = await fetch(`${API_BASE_URL}/api/habits/suggest`); // Updated from /learn to /suggest
        const data = await res.json();
        setHabits(data.recommendations || []);
      } catch (error) {
        console.error("Error fetching habits", error);
      } finally {
        setLoading(false);
      }
    }

    fetchSuggestions();
  }, []);

  return (
    <div className="bg-white p-4 rounded shadow mt-4">
      <h2 className="text-lg font-semibold mb-2">💡 Recommended Habits</h2>
      {loading ? (
        <p className="text-sm text-gray-500">Loading suggestions...</p>
      ) : habits.length === 0 ? (
        <p className="text-sm text-gray-400">No suggestions available.</p>
      ) : (
        <ul className="list-disc pl-5 space-y-1 text-sm">
          {habits.map((habit, i) => (
            <li key={i}>{habit}</li>
          ))}
        </ul>
      )}
    </div>
  );
}