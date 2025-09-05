// next/app/page.tsx
import Link from "next/link";

export default function HomePage() {
  return (
    <div className="text-center py-20">
      <h1 className="text-4xl font-bold mb-4">Welcome to AIDPA</h1>
      <p className="text-lg text-gray-600 mb-8">Your AI-Integrated Decentralized Personal Assistant</p>

      <div className="flex flex-col sm:flex-row justify-center gap-4">
        <Link href="/tasks" className="bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700">Manage Tasks</Link>
        <Link href="/health" className="bg-green-600 text-white px-6 py-3 rounded hover:bg-green-700">Health Analysis</Link>
        <Link href="/finance" className="bg-yellow-600 text-white px-6 py-3 rounded hover:bg-yellow-700">Finance</Link>
        <Link href="/assistant" className="bg-purple-600 text-white px-6 py-3 rounded hover:bg-purple-700">Chat Assistant</Link>
      </div>
    </div>
  );
}
