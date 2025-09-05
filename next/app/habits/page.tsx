import HabitSuggestion from "@/components/HabitSuggestion";

export default function HabitsPage() {
  return (
    <div className="min-h-screen p-6 bg-gray-50">
      <h1 className="text-2xl font-bold mb-4">Your Habits</h1>
      <HabitSuggestion />
    </div>
  );
}
