import { BiometricsSectionProps } from "@/types/my-plan";

const genderOptions = [
  { value: "male", label: "Male" },
  { value: "female", label: "Female" },
];

const bodyTypeOptions = [
  { value: "lean", label: "Lean" },
  { value: "normal", label: "Normal" },
  { value: "stocky", label: "Stocky" },
  { value: "obese", label: "Obese" },
];

export default function BiometricsSection({ data, onChange }: BiometricsSectionProps) {
  return (
    <section className="bg-gradient-to-br from-green-950/70 to-green-900/50 rounded-xl p-6">
      <h2 className="text-xl font-bold mb-6">Body Data</h2>
      <div className="grid md:grid-cols-3 gap-6">
        <label className="flex flex-col gap-2">
          <span className="text-text-secondary text-sm font-medium">Birth Date</span>
          <input
            type="date"
            value={data.birth_date || ""}
            onChange={e => onChange("birth_date", e.target.value)}
            className="w-full bg-surface-dark border border-surface-border rounded-lg h-12 px-4 text-white"
            max={new Date().toISOString().split("T")[0]}
          />
        </label>
        <label className="flex flex-col gap-2">
          <span className="text-text-secondary text-sm font-medium">Weight</span>
          <div className="relative">
            <input
              type="number"
              value={data.weight || ""}
              onChange={e => onChange("weight", Number(e.target.value))}
              className="w-full bg-surface-dark border border-surface-border rounded-lg h-12 px-4"
            />
            <span className="absolute right-4 top-3 text-sm text-text-secondary">kg</span>
          </div>
        </label>
        <label className="flex flex-col gap-2">
          <span className="text-text-secondary text-sm font-medium">Height</span>
          <div className="relative">
            <input
              type="number"
              value={data.height || ""}
              onChange={e => onChange("height", Number(e.target.value))}
              className="w-full bg-surface-dark border border-surface-border rounded-lg h-12 px-4"
            />
            <span className="absolute right-4 top-3 text-sm text-text-secondary">cm</span>
          </div>
        </label>
        {/* Campo Gender como botones tipo toggle */}
        <div className="flex flex-col gap-2">
          <span className="text-text-secondary text-sm font-medium">Gender</span>
          <div className="flex gap-2">
            {genderOptions.map((opt) => (
              <button
                key={opt.value}
                type="button"
                onClick={() => onChange("gender", opt.value)}
                className={`flex-1 p-3 rounded-xl border transition text-sm cursor-pointer hover:bg-primary/10 hover:text-primary hover:border-primary ${
                  data.gender === opt.value
                    ? "bg-primary text-black font-bold border-primary"
                    : "bg-surface-dark text-text-secondary border-surface-border"
                }`}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>
        {/* Campo Body Type ocupa el ancho de dos columnas */}
        <div className="flex flex-col gap-2 col-span-3 md:col-span-2">
          <span className="text-text-secondary text-sm font-medium">Body Type</span>
          <div className="grid grid-cols-4 gap-2 w-full">
            {bodyTypeOptions.map((opt) => (
              <button
                key={opt.value}
                type="button"
                onClick={() => onChange("body_type", opt.value)}
                className={`w-full flex justify-center items-center p-3 rounded-xl border transition text-sm cursor-pointer hover:bg-primary/10 hover:text-primary hover:border-primary ${
                  data.body_type === opt.value
                    ? "bg-primary text-black font-bold border-primary"
                    : "bg-surface-dark text-text-secondary border-surface-border"
                }`}
              >
                <span className="text-center">{opt.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
