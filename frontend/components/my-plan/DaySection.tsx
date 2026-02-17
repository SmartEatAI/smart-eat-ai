import { Mea_Culpa } from "next/font/google";
import Button from "../ui/Button";
import RecipeCard from "../ui/cards/recipe-card";
import { RotateCw } from "lucide-react";
import MealItem from "./MealItem";

type Meal = {
  title: string;
  calories: number;
  description: string;
  image?: string;
};

type Day = {
  name: string;
  meals: Meal[];
};

export default function DaySection({ day }: { day: Day }) {
  return (
    <section id={day.name.toLowerCase()} className="flex flex-col gap-4 px-6 scroll-mt-[20vh]">
      <h3 className="text-xl font-bold">
        {day.name}
      </h3>


      <div className="flex flex-wrap gap-4 w-full">
        {day.meals.map((items, i) => (
          <div
            key={i}
            className="flex-1 min-w-[220px] max-w-[350px]"
          >
            <MealItem meal={items} />
          </div>
        ))}
      </div>
    </section>
  );
}
