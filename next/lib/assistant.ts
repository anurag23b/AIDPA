// lib/assistant.ts
export async function sendAssistantMessage(message: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/assistant/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  });

  const data = await res.json();
  return data?.response || "AIDPA failed to respond";
}

export async function askAssistant(message: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/assistant/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: message }),
  });

  const data = await res.json();
  return data.response;
}

export async function sendVoiceAssistant(audioData: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/assistant/voice`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ audio_data: audioData }),
  });

  const data = await res.json();
  return data;
}