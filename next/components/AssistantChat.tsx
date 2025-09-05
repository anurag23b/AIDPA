"use client";

import { useState } from "react";
import { sendAssistantMessage } from "@/lib/assistant";

export default function AssistantChat() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState<string[]>([]);

  const askAssistant = async () => {
    try {
      const reply = await sendAssistantMessage(query);
      setResponse((prev) => [...prev, `You: ${query}`, `AIDPA: ${reply}`]);
    } catch (e: any) {
      setResponse((prev) => [...prev, `You: ${query}`, `⚠️ Error: ${e.message}`]);
    }

    setQuery("");
  };

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h2 className="text-xl font-bold mb-2">Talk to AIDPA</h2>
      <div className="border p-4 rounded-md bg-gray-50 h-64 overflow-auto mb-2">
        {response.map((msg, i) => (
          <div key={i} className="text-sm mb-1">{msg}</div>
        ))}
      </div>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && askAssistant()}
        placeholder="Ask something..."
        className="border p-2 w-full rounded-md"
      />
    </div>
  );
}
