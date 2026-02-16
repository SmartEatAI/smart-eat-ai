import { useState } from "react";

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

  const [activityLevel, setActivityLevel] = useState(3);

  const getLevelLabel = (value: number) => {
    switch (value) {
      case 1:
        return "Sedentario";
      case 2:
        return "Ligero";
      case 3:
        return "Moderado";
      case 4:
        return "Activo";
      case 5:
        return "Atleta";
      default:
        return "";
    }
  };

  return (
    <section className="bg-[#15201b] border border-surface-border rounded-xl p-6">
      <h2 className="text-xl font-bold mb-6">Objetivo Principal</h2>

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
          <label className="text-white font-medium">Nivel de Actividad</label>
          <span className="text-primary text-sm font-bold bg-primary/10 px-3 py-1 rounded-full">
            {getLevelLabel(activityLevel)}
          </span>
        </div>

        <input
          className="w-full bg-surface-dark"
          type="range"
          min={1}
          max={5}
          value={activityLevel}
          onChange={(e) => setActivityLevel(Number(e.target.value))}
        />

        <div className="flex justify-between text-xs text-text-secondary mt-2 font-medium">
          <span>Sedentario</span>
          <span>Ligero</span>
          <span>Moderado</span>
          <span>Activo</span>
          <span>Atleta</span>
        </div>
      </div>
    </section>
  );
}
