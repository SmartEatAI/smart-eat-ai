type Props = {
  title: string;
  value: string;
  unit?: string;
};

export default function StatsCard({ title, value, unit }: Props) {
  return (
    <div className="rounded-xl p-5 bg-surface-dark border border-[#283930]">
      <p className="text-xs uppercase text-[#9db9ab] font-bold">
        {title}
      </p>
      <div className="flex items-baseline gap-2">
        <p className="text-2xl font-bold">{value}</p>
        {unit && <p className="text-sm text-[#9db9ab]">{unit}</p>}
      </div>
    </div>
  );
}
