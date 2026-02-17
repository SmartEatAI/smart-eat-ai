import MealCard from "./MealCard";

type Meal = {
  title: string;
  kcal: number;
  description: string;
};

type Day = {
  name: string;
  date: number;
  meals: Meal[];
};

export default function DaySection({ day }: { day: Day }) {
  return (
    <section className="flex flex-col gap-4">
      <h3 className="text-xl font-bold">
        {day.name}, {day.date}
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {day.meals.map((meal, i) => (
          <MealCard key={i} meal={meal} />
        ))}
      </div>
    </section>
  );
}
