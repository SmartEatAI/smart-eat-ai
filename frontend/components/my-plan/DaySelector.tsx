import { useState } from "react";
import Button from "../ui/Button";

type Day = {
  name: string;
};

export default function DaySelector({ days }: { days: Day[] }) {
  const [selectedDay, setSelectedDay] = useState(days[0].name.toLowerCase());


  return (
    <div className="flex overflow-x-auto scrollbar-hide gap-2 py-8 justify-center">
      {days.map((day, i) => (
        <a
          key={i}
          href={`#${day.name.toLowerCase()}`}
          className="shrink-0"
          onClick={() => setSelectedDay(day.name.toLowerCase())}
        >
          <Button
            variant="day"
            className={`${
              selectedDay === day.name.toLowerCase()
                ? "bg-primary text-black"
                : "bg-surface-dark text-[#9db9ab]"
            }`}
          >
            <span className="text-xs uppercase">{day.name}</span>
          </Button>
        </a>
      ))}
    </div>
  );
}
