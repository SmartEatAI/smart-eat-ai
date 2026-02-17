type Props = {
  data: any;
  onChange: (field: string, value: number) => void;
};

export default function BiometricsSection({ data, onChange }: Props) {
  const inputs = [
    { label: "Edad", field: "age", unit: "años" },
    { label: "Peso", field: "weight", unit: "kg" },
    { label: "Altura", field: "height", unit: "cm" },
  ];

  return (
    <section className="bg-[#15201b] border border-surface-border rounded-xl p-6">
      <h2 className="text-xl font-bold mb-6">Datos Corporales</h2>

      <div className="grid md:grid-cols-3 gap-6">
        {inputs.map((input) => (
          <label key={input.field} className="flex flex-col gap-2">
            <span className="text-text-secondary text-sm">
              {input.label}
            </span>

            <div className="relative">
              <input
                type="number"
                value={data[input.field] || ""}
                onChange={(e) =>
                  onChange(input.field, Number(e.target.value))
                }
                className="w-full bg-surface-dark border border-surface-border rounded-lg h-12 px-4"
              />
              <span className="absolute right-4 top-3 text-sm text-text-secondary">
                {input.unit}
              </span>
            </div>
          </label>
        ))}
      </div>
    </section>
  );
}
