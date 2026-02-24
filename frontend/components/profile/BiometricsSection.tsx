type Props = {
  data: any;
  onChange: (field: string, value: any) => void;
};

export default function BiometricsSection({ data, onChange }: Props) {
  return (
    <section className="bg-[#15201b] border border-surface-border rounded-xl p-6">
      <h2 className="text-xl font-bold mb-6">Body Data</h2>
      <div className="grid md:grid-cols-3 gap-6">
        <label className="flex flex-col gap-2">
          <span className="text-text-secondary text-sm">Birth Date</span>
          <input
            type="date"
            value={data.birth_date || ""}
            onChange={e => onChange("birth_date", e.target.value)}
            className="w-full bg-surface-dark border border-surface-border rounded-lg h-12 px-4 text-white"
            max={new Date().toISOString().split("T")[0]}
          />
        </label>
        <label className="flex flex-col gap-2">
          <span className="text-text-secondary text-sm">Weight</span>
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
          <span className="text-text-secondary text-sm">Height</span>
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
      </div>
    </section>
  );
}
