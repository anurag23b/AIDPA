"use client";

import React, { useState, useEffect } from "react";
import TaskList from "./TaskList";
import TaskSummary from "./TaskSummary";
import TaskCommandInput from "./TaskCommandInput";
import { Task } from "@/types/tasks";
import { logTask, getTasks } from "@/lib/tasks";

export default function TaskForm() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [schedule, setSchedule] = useState("daily");
  const [priority, setPriority] = useState("normal");
  const [description, setDescription] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [tags, setTags] = useState<string>("");

  const [repeat, setRepeat] = useState<"none" | "daily" | "weekly" | "monthly">("none");
  const [searchText, setSearchText] = useState("");
  const [tagFilter, setTagFilter] = useState("");
  const [filterPriority, setFilterPriority] = useState("");
  const [filterSchedule, setFilterSchedule] = useState("");
  const [sortBy, setSortBy] = useState("");

  useEffect(() => {
    const loadTasks = async () => {
      const res = await getTasks();
      setTasks(res);
    };
    loadTasks();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const newTask: Task = {
      title,
      description,
      schedule,
      priority,
      due_date: dueDate || undefined,
      repeat,
      tags: tags.split(",").map((tag) => tag.trim()).filter(Boolean),
    };

    const saved = await logTask(newTask);
    setTasks((prev) => [...prev, saved]);

    // Reset form
    setTitle("");
    setDescription("");
    setDueDate("");
    setPriority("normal");
    setSchedule("daily");
    setTags("");
    setRepeat("none");
  };

  const filteredTasks = tasks
    .filter((task) =>
      searchText
        ? task.title?.toLowerCase().includes(searchText.toLowerCase()) ||
          task.description?.toLowerCase().includes(searchText.toLowerCase())
        : true
    )
    .filter((task) =>
      tagFilter
        ? (task.tags || []).some((tag) =>
            tag.toLowerCase().includes(tagFilter.toLowerCase())
          )
        : true
    )
    .filter((task) => (filterPriority ? task.priority === filterPriority : true))
    .filter((task) => (filterSchedule ? task.schedule === filterSchedule : true))
    .sort((a, b) => {
      if (sortBy === "due_date") {
        return (a.due_date || "").localeCompare(b.due_date || "");
      }
      if (sortBy === "title") {
        return a.title.localeCompare(b.title);
      }
      return 0;
    });

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-md">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">Create a New Task</h2>

      <form onSubmit={handleSubmit} className="space-y-4 mb-8">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Task title"
          className="border border-gray-300 p-2 w-full rounded-md"
          required
        />
        <input
          value={tags}
          onChange={(e) => setTags(e.target.value)}
          placeholder="Tags (comma separated)"
          className="border border-gray-300 p-2 w-full rounded-md"
        />
        <input
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          placeholder="Search title or description"
          className="border p-2 rounded-md w-full"
        />
        <input
          value={tagFilter}
          onChange={(e) => setTagFilter(e.target.value)}
          placeholder="Filter by tag"
          className="border p-2 rounded-md w-full"
        />

        <select
          value={repeat}
          // TaskForm.tsx
          onChange={(e) => setRepeat(e.target.value as "none" | "daily" | "weekly" | "monthly")}

          className="border p-2 w-full rounded-md"
        >
          <option value="none">No Repeat</option>
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>

        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Description (optional)"
          className="border border-gray-300 p-2 w-full rounded-md"
        />

        <div className="grid grid-cols-2 gap-4">
          <select
            value={schedule}
            onChange={(e) => setSchedule(e.target.value)}
            className="border p-2 w-full rounded-md"
          >
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="one-time">One-Time</option>
          </select>

          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            className="border p-2 w-full rounded-md"
          >
            <option value="low">Low Priority</option>
            <option value="normal">Normal</option>
            <option value="high">High Priority</option>
          </select>
        </div>

        <input
          type="date"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
          className="border p-2 w-full rounded-md"
        />

        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
        >
          Add Task
        </button>
      </form>

      <div className="flex flex-wrap gap-4 mb-4 items-center">
        <select
          onChange={(e) => setFilterPriority(e.target.value)}
          className="border p-2 rounded-md"
        >
          <option value="">All Priorities</option>
          <option value="high">High</option>
          <option value="normal">Normal</option>
          <option value="low">Low</option>
        </select>

        <select
          onChange={(e) => setFilterSchedule(e.target.value)}
          className="border p-2 rounded-md"
        >
          <option value="">All Schedules</option>
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="one-time">One-Time</option>
        </select>

        <select
          onChange={(e) => setSortBy(e.target.value)}
          className="border p-2 rounded-md"
        >
          <option value="">Sort By</option>
          <option value="due_date">Due Date</option>
          <option value="title">Title</option>
        </select>
      </div>

      <TaskCommandInput onNewTask={(task) => setTasks((prev) => [...prev, task])} />
      <TaskSummary tasks={tasks} />
      <TaskList tasks={filteredTasks} setTasks={setTasks} />
    </div>
  );
}
