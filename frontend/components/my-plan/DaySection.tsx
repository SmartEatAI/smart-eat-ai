import { Day } from "@/types/my-plan";
import MealItem from "./MealItem";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";

export default function DaySection({
  day,
  dayIndex,
  onSwapMeal,
  onAcceptSwap,
}: {
  day: Day;
  dayIndex: number;
  onSwapMeal: (dayIndex: number, mealIndex: number) => void;
  onAcceptSwap: (dayIndex: number, mealIndex: number) => void;
}) {
  return (
    <section id={day.name.toLowerCase()} className="flex flex-col gap-4 scroll-mt-[20vh]">
      <h3 className="text-xl font-bold">
        {day.name}
      </h3>

      <Carousel opts={{ loop: true, align: "start" }} className="w-full">
        <CarouselContent className="-ml-2 md:-ml-4">
          {day.meals.map((meal, mealIndex) =>
            meal.recipe ? (
              <CarouselItem
                key={`meal-${dayIndex}-${mealIndex}-${meal.recipe.recipe_id}`}
                className="pl-2 md:pl-4 md:basis-1/2 lg:basis-1/3 min-w-[220px] max-w-[350px] w-full"
              >
                <MealItem
                  meal={meal}
                  onConfirm={() => onAcceptSwap(dayIndex, mealIndex)}
                  onRequestSwap={() => onSwapMeal(dayIndex, mealIndex)}
                />
              </CarouselItem>
            ) : null
          )}
        </CarouselContent>
        <CarouselPrevious className="hidden lg:flex left-2" />
        <CarouselNext className="hidden lg:flex right-2" />
      </Carousel>
    </section>
  );
}
