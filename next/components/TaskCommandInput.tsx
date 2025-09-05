"use client";

import React, { useState } from "react";
import { analyzeTask } from "@/lib/nlp";
import { logTask } from "@/lib/tasks";
import { Task } from "@/types/tasks";

export default function TaskCommandInput({ onNewTask }: { onNewTask: (task: Task) => void }) {
  const [input, setInput] = useState("");
  const [listening, setListening] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    try {
      setLoading(true);
      const parsed: Task = await analyzeTask(input);
      const saved = await logTask(parsed);
      onNewTask(saved);
      setInput("");
    } catch (err) {
      alert("Failed to create task from input.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const startVoice = () => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("Speech recognition not supported");
      return;
    }
    const recognition = new (window as any).webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event: any) => {
      setInput(event.results[0][0].transcript);
    };

    recognition.onerror = (e: any) => console.error(e);
    recognition.onend = () => setListening(false);

    recognition.start();
    setListening(true);
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-2 mb-4">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="e.g. Remind me to drink water every 2 hours"
        className="flex-1 p-2 border rounded"
      />
      <button
        type="button"
        onClick={startVoice}
        className={`px-3 py-2 rounded ${listening ? "bg-red-500" : "bg-gray-200 hover:bg-blue-500 text-black"}`}
      >
        🎤
      </button>
      <button
        type="submit"
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        {loading ? "Creating..." : "Submit"}
      </button>
    </form>
  );
}
