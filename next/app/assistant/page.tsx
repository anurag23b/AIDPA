"use client";

import VoiceChat from "@/components/VoiceChat";
import AssistantChat from "@/components/AssistantChat";
import AssistantFeed from "@/components/AssistantFeed";

export default function AssistantPage() {
  return (
    <div className="min-h-screen bg-gray-100 p-4 space-y-6">
      <h1 className="text-2xl font-bold text-center text-gray-800">AIDPA Assistant</h1>
      
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white p-4 rounded-xl shadow-md">
          <h2 className="text-lg font-semibold mb-2">🎙️ Voice Assistant</h2>
          <VoiceChat />
        </div>
        <div className="bg-white p-4 rounded-xl shadow-md">
          <h2 className="text-lg font-semibold mb-2">💬 Chat Assistant</h2>
          <AssistantChat />
        </div>
      </div>

      <AssistantFeed />
    </div>
  );
}
