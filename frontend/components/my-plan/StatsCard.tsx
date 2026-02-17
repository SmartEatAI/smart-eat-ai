type Props = {
  title: string;
  value: string;
  unit?: string;
  bgColor?: string; // Clase Tailwind para el fondo
  icon?: React.ReactNode; // Icono opcional
};

export default function StatsCard({ title, value, unit, bgColor = "bg-surface-dark", icon }: Props) {
  return (
    <div className={`rounded-xl p-5 border border-[#283930] flex items-center gap-4 ${bgColor}`}>
      {icon && (
        <div className="text-2xl flex-shrink-0">
          {icon}
        </div>
      )}
      <div>
        <p className="text-xs uppercase text-[#9db9ab] font-bold">
          {title}
        </p>
        <div className="flex items-baseline gap-2">
          <p className="text-2xl font-bold">{value}</p>
          {unit && <p className="text-sm text-[#9db9ab]">{unit}</p>}
        </div>
      </div>
    </div>
  );
}