import { GoalSectionProps } from "@/types/my-plan";

const activityLevels = [
  { value: "low", label: "Sedentary" },
  { value: "medium", label: "Moderate" },
  { value: "high", label: "Active" },
];

const goals = [
  { id: "lose_weight", label: "Lose Fat" },
  { id: "maintain_weight", label: "Maintain" },
  { id: "gain_weight", label: "Gain Muscle" },
];

export default function GoalSection({ goal, setGoal, activityLevel, setActivityLevel }: GoalSectionProps) {
  return (
    <section className="bg-gradient-to-br from-green-950/70 to-green-900/50 rounded-xl p-6">
      <h2 className="text-xl font-bold mb-6">Main Goal</h2>

      <div className="grid md:grid-cols-3 gap-4 mb-6">
        {goals.map((g) => (
          <button
            key={g.id}
            onClick={() => setGoal(g.id)}
            className={`cursor-pointer p-4 rounded-xl border transition text-sm hover:bg-primary/10 hover:text-primary hover:border-primary ${
              goal === g.id
                ? "bg-primary text-black font-bold border-primary"
                : "bg-surface-dark text-text-secondary border-surface-border"
            }`}
          >
            {g.label}
          </button>
        ))}
      </div>

      <div className="pt-6 border-t border-surface-border/50">
        <div className="flex justify-between items-end mb-4">
          <label className="text-xl font-bold">Activity Level</label>
        </div>

        <div className="flex gap-2">
          {activityLevels.map((a) => (
            <button
              key={a.value}
              onClick={() => setActivityLevel(a.value)}
              className={`cursor-pointer flex-1 p-4 rounded-xl border transition text-sm hover:bg-primary/10 hover:text-primary hover:border-primary ${
                activityLevel === a.value
                  ? "bg-primary text-black font-bold border-primary"
                  : "bg-surface-dark text-text-secondary border-surface-border"
              }`}
            >
              {a.label}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
