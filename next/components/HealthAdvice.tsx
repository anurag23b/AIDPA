import React from "react";

export default function HealthAdvice({ tips }: { tips: string[] }) {
  return (
    <div className="bg-blue-100 p-4 rounded">
      <h3 className="font-bold mb-2">Tips</h3>
      <ul className="list-disc list-inside text-sm">
        {tips.map((tip, i) => (
          <li key={i}>{tip}</li>
        ))}
      </ul>
    </div>
  );
}
