"use client";

import React, { useState } from "react";
import { analyzeHealth } from "@/lib/health";
import HealthResult from "./HealthResult";
import axios from "axios";
import HealthAdvice from "./HealthAdvice";
import HealthChart from "./HealthChart";

export default function HealthForm() {
  const [input, setInput] = useState("");
  type HealthResultType = {
    status: string;
    recommendations: string[];
  };

  const [result, setResult] = useState<HealthResultType | null>(null);
  const [loading, setLoading] = useState(false);
  const [chart, setChart] = useState<{ date: string; value: number }[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await analyzeHealth(input);
        setResult({
          status: res.status,
          recommendations: res.recommendations
        });
        setChart(res.chart);
    } catch (err) {
      console.error("Health analyze error:", err);
    }
    setLoading(false);
  };



  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="flex flex-col gap-2">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe symptoms, routines, etc."
          className="border rounded p-2 h-32"
        />
        <button
          type="submit"
          className="bg-green-600 text-white px-4 py-2 rounded self-start"
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Submit"}Analyze
        </button>
      </form>
      {result && (
        <div className="mt-4 space-y-4">
          <HealthResult summary={result.status} />
          <HealthAdvice tips={result.recommendations} />
          {chart.length > 0 && <HealthChart data={chart} />}
        </div>
      )}

    </div>
  );
}
