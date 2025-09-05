import { getUserId } from "@/lib/session";

if (!process.env.NEXT_PUBLIC_API_URL) {
  throw new Error("API base URL is not defined!");
}
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export async function analyzeHealth(input: string) {
  const res = await fetch(`${API_BASE_URL}/api/health/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-User-ID": getUserId() },
    body: JSON.stringify({ data: input }),
  });
  if (!res.ok) throw new Error("Health analysis failed");
  return await res.json();
}

export async function fetchHealthHistory() {
  const res = await fetch(`${API_BASE_URL}/api/health/history`, {
    headers: { "X-User-ID": getUserId() },
  });
  if (!res.ok) throw new Error("Failed to fetch history");
  return await res.json();
}

// New function for prediction
export async function predictHealth(data: { records: { steps: number; heart_rate: number; sleep_hours: number }[] }) {
  const res = await fetch(`${API_BASE_URL}/api/health/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-User-ID": getUserId() },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Prediction failed");
  return await res.json();
}