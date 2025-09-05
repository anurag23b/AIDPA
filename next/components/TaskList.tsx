"use client";

import React from "react";
import { Task } from "@/types/tasks";
import { toggleTaskComplete, deleteTask } from "@/lib/tasks";
import { format } from "date-fns";

interface Props {
  tasks: Task[];
  setTasks: React.Dispatch<React.SetStateAction<Task[]>>;
}

export default function TaskList({ tasks, setTasks }: Props) {
  const handleToggle = async (taskId: string, completed: boolean) => {
    const updated = await toggleTaskComplete(taskId, !completed);
    if (!updated) return;
    setTasks((prev) =>
      prev.map((task) =>
        task.id === taskId ? { ...task, completed: updated.completed } : task
      )
    );
  };

  const handleDelete = async (taskId: string) => {
    await deleteTask(String(taskId)); // ✅
    setTasks((prev) => prev.filter((task) => task.id !== taskId));
  };

  const getPriorityStyle = (priority: string) => {
    switch (priority) {
      case "high":
        return "bg-red-500 text-white";
      case "normal":
        return "bg-yellow-400 text-white";
      case "low":
        return "bg-green-500 text-white";
      default:
        return "bg-gray-300 text-black";
    }
  };

  return (
    <div className="space-y-4 mt-8">
      {tasks.length === 0 && (
        <p className="text-gray-600 text-center">No tasks yet. Start by adding one.</p>
      )}

      {tasks.map((task) => (
        <div
          key={task.id}
          className={`p-4 rounded-lg shadow-md border flex justify-between items-start ${
            task.completed ? "bg-gray-100 line-through text-gray-400" : "bg-white"
          }`}
        >
          <div className="flex-1">
            <h3 className="text-lg font-semibold">{task.title}</h3>
            {task.description && (
              <p className="text-sm text-gray-500">{task.description}</p>
            )}

            <div className="mt-2 flex flex-wrap items-center gap-2 text-sm">
              <span className={`px-2 py-1 rounded ${getPriorityStyle(task.priority || "normal")}`}>
                {task.priority || "normal"}
              </span>
              <span className="text-blue-600 font-medium capitalize">
                {task.schedule}
              </span>
              {task.due_date && (
                <span className="text-gray-600">
                  Due: {format(new Date(task.due_date), "MMM d, yyyy")}
                </span>
              )}
            </div>

            {Array.isArray(task.tags) && task.tags.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-2">
                {task.tags.map((tag, idx) => (
                  <span key={idx} className="text-xs bg-gray-200 px-2 py-0.5 rounded-full">
                    #{tag}
                  </span>
                ))}
              </div>
            )}
          </div>

          <div className="flex flex-col items-center ml-4 space-y-2">
            <button
              onClick={() => handleToggle(task.id!, task.completed || false)}
              className={`px-2 py-1 rounded text-xs ${
                task.completed
                  ? "bg-green-300 text-green-900"
                  : "bg-gray-200 hover:bg-blue-500 hover:text-white"
              }`}
            >
              {task.completed ? "Undo" : "Done"}
            </button>

            <button
              onClick={() => handleDelete(task.id!)}
              className="text-xs text-red-500 hover:underline"
            >
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
