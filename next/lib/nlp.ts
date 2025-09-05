import { getUserId } from "@/lib/session";

if (!process.env.NEXT_PUBLIC_API_URL) {
  throw new Error("API base URL is not defined!");
}
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export async function analyzeTask(prompt: string) {
  const res = await fetch(`${API_BASE_URL}/api/tasks/parse`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-User-ID": getUserId(),
    },
    body: JSON.stringify({ raw_input: prompt }),
  });

  if (!res.ok) throw new Error("Failed to parse task");
  return await res.json();
}
