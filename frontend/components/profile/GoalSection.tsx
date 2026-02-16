type Props = {
  goal: string;
  setGoal: (goal: string) => void;
};

export default function GoalSection({ goal, setGoal }: Props) {
  const goals = [
    { id: "lose", label: "Perder Grasa" },
    { id: "maintain", label: "Mantener" },
    { id: "gain", label: "Ganar Músculo" },
  ];

  return (
    <section className="bg-[#15201b] border border-surface-border rounded-xl p-6">
      <h2 className="text-xl font-bold mb-6">
        Objetivo Principal
      </h2>

      <div className="grid md:grid-cols-3 gap-4">
        {goals.map((g) => (
          <button
            key={g.id}
            onClick={() => setGoal(g.id)}
            className={`p-4 rounded-xl border transition
              ${
                goal === g.id
                  ? "border-primary bg-primary/10"
                  : "border-surface-border bg-surface-dark"
              }`}
          >
            {g.label}
          </button>
        ))}
      </div>
    </section>
  );
}
