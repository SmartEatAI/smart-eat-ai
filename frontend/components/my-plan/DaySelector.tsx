import { useState } from "react";
import Button from "../ui/Button";
import { useRef, useEffect } from "react";
import { Day } from "@/types/my-plan";

export default function DaySelector({ days }: { days: Day[] }) {
  const [selectedDay, setSelectedDay] = useState(
    days && days.length > 0 && days[0]?.name ? days[0].name.toLowerCase() : ""
  );
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollLeft = 0;
    }
  }, []);


  return (
    <div ref={scrollRef} className="flex min-w-0 overflow-x-auto scrollbar-hide gap-2 py-10 pl-4 pr-4 snap-x md:justify-center">
      {days.map((day, i) => (
        <a
          key={i}
          href={`#${day.name.toLowerCase()}`}
          className="shrink-0 snap-start"
          onClick={() => setSelectedDay(day.name.toLowerCase())}
        >
          <Button
            variant="secondary"
            className={`${
              selectedDay === day.name.toLowerCase()
                ? "bg-green-500 text-black"
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
