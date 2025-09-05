"use client";

import React, { useState, useEffect } from "react";
import { Sparkles, User, Bot } from "lucide-react";

if (!process.env.NEXT_PUBLIC_API_URL) {
  throw new Error("API base URL is not defined!");
}
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

interface Message {
  role: "user" | "assistant";
  content: string;
  type?: "task" | "finance" | "health" | "general";
}

const iconForType = (type?: string) => {
  switch (type) {
    case "task": return <span className="text-blue-500 text-xs ml-2">(Task)</span>;
    case "finance": return <span className="text-green-500 text-xs ml-2">(Finance)</span>;
    case "health": return <span className="text-rose-500 text-xs ml-2">(Health)</span>;
    default: return <span className="text-gray-400 text-xs ml-2">(General)</span>;
  }
};

export default function AssistantFeed() {
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    async function fetchFeed() {
      try {
        const res = await fetch(`${API_BASE_URL}/api/assistant/history`);
        const data = await res.json();
        setMessages(data);
      } catch (error) {
        console.error("Error fetching assistant history", error);
      }
    }
    fetchFeed();
    const interval = setInterval(fetchFeed, 5000); // Poll every 5s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="rounded-2xl shadow-md w-full max-w-2xl mx-auto my-4 bg-white p-6">
      <h2 className="text-xl font-semibold mb-4 flex items-center gap-2 text-purple-600">
        <Sparkles className="w-5 h-5" /> Assistant Feed
      </h2>
      <div className="h-[300px] overflow-y-auto pr-2 space-y-4">
        {messages.length === 0 ? (
          <p className="text-gray-600">No messages yet.</p>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className="flex items-start gap-3">
              {msg.role === "user" ? (
                <User className="w-5 h-5 text-sky-600 mt-1" />
              ) : (
                <Bot className="w-5 h-5 text-purple-500 mt-1" />
              )}
              <div>
                <p className="text-sm font-medium">
                  {msg.role === "user" ? "You" : "Assistant"}
                  {msg.role === "assistant" && iconForType(msg.type)}
                </p>
                <p className="text-sm text-gray-600">{msg.content}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}