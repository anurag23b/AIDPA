import React from "react";

type Props = {
  summary: string;
};

export default function HealthResult({ summary }: Props) {
  return (
    <div className="bg-white border rounded p-4 shadow">
      <h3 className="font-semibold mb-2">Health Summary</h3>
      <p className="text-sm text-gray-800 whitespace-pre-line">{summary}</p>
    </div>
  );
}
