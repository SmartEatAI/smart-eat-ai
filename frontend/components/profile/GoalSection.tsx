type Props = {
  goal: string;
  setGoal: (goal: string) => void;
  activityLevel: string;
  setActivityLevel: (level: string) => void;
};

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

export default function GoalSection({ goal, setGoal, activityLevel, setActivityLevel }: Props) {
  return (
    <section className="bg-[#15201b] border border-surface-border rounded-xl p-6">
      <h2 className="text-xl font-bold mb-6">Main Goal</h2>

      <div className="grid md:grid-cols-3 gap-4 mb-6">
        {goals.map((g) => (
          <button
            key={g.id}
            onClick={() => setGoal(g.id)}
            className={`p-4 rounded-xl border transition ${
              goal === g.id
                ? "border-primary bg-primary/10"
                : "border-surface-border bg-surface-dark"
            }`}
          >
            {g.label}
          </button>
        ))}
      </div>

      <div className="pt-6 border-t border-surface-border/50">
        <div className="flex justify-between items-end mb-4">
          <label className="text-white font-medium">Activity Level</label>
          <span className="text-primary text-sm font-bold bg-primary/10 px-3 py-1 rounded-full">
            {activityLevels.find((a) => a.value === activityLevel)?.label || ""}
          </span>
        </div>

        <div className="flex gap-2">
          {activityLevels.map((a) => (
            <button
              key={a.value}
              onClick={() => setActivityLevel(a.value)}
              className={`flex-1 py-2 rounded-md text-sm transition ${
                activityLevel === a.value
                  ? "bg-primary text-black font-bold"
                  : "bg-surface-dark text-text-secondary"
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
