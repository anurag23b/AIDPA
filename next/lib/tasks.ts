import { Task } from "@/types/tasks";
import { getUserId } from "@/lib/session";

if (!process.env.NEXT_PUBLIC_API_URL) {
  throw new Error("API base URL is not defined!");
}
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;
const BASE = `${API_BASE_URL}/api/tasks`;

export async function logTask(task: Task): Promise<Task> {
  if (!task.title || !task.priority || !task.category) {
    throw new Error("Invalid task object");
  }
  const res = await fetch(BASE, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-User-ID": getUserId(),
    },
    body: JSON.stringify(task),
  });

  if (!res.ok) throw new Error("Failed to log task");
  return res.json();
}

export async function getTasks(): Promise<Task[]> {
  const res = await fetch(BASE, {
    headers: { "X-User-ID": getUserId() },
  });
  
  if (!res.ok) throw new Error("Failed to fetch tasks");
  return res.json();
}

export async function deleteTask(id: string): Promise<void> {
  const res = await fetch(`${BASE}/${id}`, {
    method: "DELETE",
    headers: { "X-User-ID": getUserId() },
  });
  if (!res.ok) throw new Error("Failed to delete task");
}

export async function toggleTaskComplete(id: string, completed: boolean): Promise<Task | null> {
  const res = await fetch(`${BASE}/${id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "X-User-ID": getUserId(),
    },
    body: JSON.stringify({ completed }),
  });
  if (!res.ok) throw new Error("Failed to update task");
  const updated = await res.json();

  // Handle repeat
  if (completed && updated.repeat && updated.repeat !== "none") {
    const nextDue = getNextDueDate(updated.due_date, updated.repeat);
    const cloned = {
      ...updated,
      completed: false,
      due_date: nextDue,
      category: updated.category || "general",
    };
    delete cloned.id;
    await logTask(cloned);
  }

  return updated;
}

function getNextDueDate(current: string, repeat: string): string {
  const now = new Date(current);
  if (repeat === "daily") now.setDate(now.getDate() + 1);
  else if (repeat === "weekly") now.setDate(now.getDate() + 7);
  else if (repeat === "monthly") now.setMonth(now.getMonth() + 1);
  return now.toISOString();
}
