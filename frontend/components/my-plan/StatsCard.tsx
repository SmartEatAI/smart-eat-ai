import { StatsCardProps } from "@/types/my-plan";

export default function StatsCard({
  title,
  current,
  goal,
  unit,
  bgColor = "bg-gradient-to-br from-green-950/80 to-green-900/60 border-green-800/50",
  icon,
}: StatsCardProps) {
  // Determinar si current supera goal (ambos numéricos)
  const isOverGoal =
    typeof current === "number" && typeof goal === "number" && current > goal;

  // Usar color destructivo si se supera el objetivo, si no, color normal
  const currentColor = isOverGoal
    ? "text-[color:var(--destructive)]"
    : "text-primary";

  return (
    <div className={`rounded-xl p-4 sm:p-5 border flex items-center gap-3 sm:gap-4 ${bgColor}`}>
      {icon && (
        <div className="text-xl sm:text-2xl flex-shrink-0">
          {icon}
        </div>
      )}
      <div className="flex-1 min-w-0">
        <p className="text-xs uppercase text-[#9db9ab] font-bold truncate">
          {title}
        </p>
        <div className="flex items-baseline gap-1.5 sm:gap-2 flex-wrap">
          <p className={`text-xl sm:text-2xl font-bold ${currentColor}`}>{current}</p>
          <span className="text-base sm:text-lg font-bold text-[#9db9ab]">/</span>
          <p className="text-xl sm:text-2xl font-bold text-chart-2">{goal}</p>
          {unit && <p className="text-xs sm:text-sm text-[#9db9ab]">{unit}</p>}
        </div>
      </div>
    </div>
  );
}