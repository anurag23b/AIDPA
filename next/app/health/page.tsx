import React from "react";
import HealthForm from "@/components/HealthForm";
import HealthHistory from "@/components/HealthHistory";
import HabitSuggestion from "@/components/HabitSuggestion";

export default function HealthPage() {
  return (
    <main className="p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Health Assistant</h1>
      <HealthForm />
      <HealthHistory />
      <HabitSuggestion />
    </main>
  );
}
