// next/components/VoiceChat.tsx
"use client";

import { useState, useRef } from "react";
import { getUserId } from "@/lib/session";

declare global {
  interface Window {
    MediaRecorder: any;
  }
}

export default function VoiceChat() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [listening, setListening] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const isMediaSupported = typeof window !== "undefined" && "MediaRecorder" in window && "mediaDevices" in navigator && "getUserMedia" in navigator.mediaDevices;

  const startRecording = () => {
    if (!isMediaSupported) {
      setResponse("⚠️ Voice recording not supported in this browser or context");
      return;
    }

    navigator.mediaDevices.getUserMedia({ audio: true })
      .then((stream) => {
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;
        audioChunksRef.current = [];

        mediaRecorder.ondataavailable = (event) => {
          audioChunksRef.current.push(event.data);
        };

        mediaRecorder.onstop = async () => {
          const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
          const reader = new FileReader();
          reader.onloadend = async () => {
            const base64String = (reader.result as string).split(",")[1];
            const res = await fetch("/api/assistant/voice", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ audio_data: base64String }),
            });
            const data = await res.json();
            setResponse(data.response || "⚠️ No response");
          };
          reader.readAsDataURL(audioBlob);
        };

        mediaRecorder.start();
        setListening(true);
        setTimeout(() => {
          mediaRecorder.stop();
          stream.getTracks().forEach((track) => track.stop());
          setListening(false);
        }, 5000); // Record for 5 seconds
      })
      .catch((err) => setResponse(`⚠️ Error: ${err.message}`));
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h2 className="text-xl font-bold mb-2">🎙️ Talk to AIDPA</h2>
      <div className="flex gap-2 mb-4">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 border rounded p-2"
          placeholder="Ask AIDPA something..."
        />
        <button
          onClick={() =>
            fetch("/api/assistant/chat", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ message: query }),
            })
              .then((res) => res.json())
              .then((data) => setResponse(data.response))
          }
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Send
        </button>
        <button
          onClick={startRecording}
          className={`px-4 py-2 rounded ${listening ? "bg-red-600" : "bg-green-600"} text-white hover:bg-opacity-80`}
          disabled={listening || !isMediaSupported}
        >
          {listening ? "Listening..." : "🎤 Record"}
        </button>
      </div>
      <div className="bg-gray-100 p-4 rounded">{response || "..."}</div>
    </div>
  );
}