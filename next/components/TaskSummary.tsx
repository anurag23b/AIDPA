"use client";

import React from "react";
import { Task } from "@/types/tasks";

type Props = {
  tasks: Task[];
};

export default function TaskSummary({ tasks }: Props) {
  const total = tasks.length;
  const completed = tasks.filter((t) => t.completed).length;
  const daily = tasks.filter((t) => t.schedule?.includes("daily")).length;
  const weekly = tasks.filter((t) => t.schedule?.includes("weekly")).length;

  return (
    <div className="bg-gray-100 p-4 rounded mb-4">
      <h2 className="text-lg font-semibold mb-2">Task Summary</h2>
      <ul className="text-sm space-y-1">
        <li>Total Tasks: {total}</li>
        <li>Completed: {completed}</li>
        <li>Daily: {daily}</li>
        <li>Weekly: {weekly}</li>
      </ul>
    </div>
  );
}
