type Props = {
  meals: number;
  setMeals: (n: number) => void;
};

export default function PreferencesSection({
  meals,
  setMeals,
}: Props) {
  const options = [3, 4, 5, 6];

  return (
    <section className="bg-[#15201b] border border-surface-border rounded-xl p-6">
      <h2 className="text-xl font-bold mb-6">
        Preferencias
      </h2>

      <div>
        <p className="text-text-secondary text-sm mb-3">
          Comidas por día
        </p>

        <div className="flex gap-2">
          {options.map((n) => (
            <button
              key={n}
              onClick={() => setMeals(n)}
              className={`flex-1 py-2 rounded-md text-sm transition
              ${
                meals === n
                  ? "bg-primary text-black font-bold"
                  : "bg-surface-dark text-text-secondary"
              }`}
            >
              {n === 6 ? "6+" : n}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
