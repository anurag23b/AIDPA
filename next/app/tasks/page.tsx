"use client";

import React, { useEffect, useState } from "react";
import { Task } from "@/types/tasks";
import { getTasks } from "@/lib/tasks";
import TaskCommandInput from "@/components/TaskCommandInput";
import TaskSummary from "@/components/TaskSummary";
import TaskList from "@/components/TaskList";

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const fetched = await getTasks();
        setTasks(fetched);
      } catch (err) {
        console.error("Failed to fetch tasks", err);
      }
    }
    fetchData();
  }, []);

  const handleNewTask = (task: Task) => {
    setTasks((prev) => [...prev, task]);
  };

  return (
    <div className="min-h-screen p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">📋 AIDPA Tasks</h1>

      <TaskCommandInput onNewTask={handleNewTask} />
      <TaskSummary tasks={tasks} />
      <TaskList tasks={tasks} setTasks={setTasks} />
    </div>
  );
}
