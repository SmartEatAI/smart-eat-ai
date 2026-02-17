type Day = {
  name: string;
  date: number;
};

export default function DaySelector({ days }: { days: Day[] }) {
  return (
    <div className="flex overflow-x-auto gap-2 pb-2">
      {days.map((day, i) => (
        <button
          key={day.date}
          className={`min-w-[100px] p-3 rounded-xl flex flex-col items-center
          ${
            i === 0
              ? "bg-primary text-black"
              : "bg-surface-dark text-[#9db9ab]"
          }`}
        >
          <span className="text-xs uppercase">{day.name}</span>
          <span className="text-lg font-bold">{day.date}</span>
        </button>
      ))}
    </div>
  );
}
