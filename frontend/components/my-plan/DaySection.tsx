import MealItem from "./MealItem";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";

type Recipe = {
  recipe_id: number;
  name: string;
  image_url: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  meal_types: string[];
  diet_types: string[];
  recipe_url: string;
};

type MealItem = {
  recipe: Recipe;
  meal_type: string;
  swapSuggestion?: Recipe; // alternativa sugerida por swap
  accepted?: boolean; // si el usuario aceptó la sugerencia
};

type DayPlan = {
  name: string;
  meals: MealItem[];
};
type Meal = {
  recipe: Recipe;
  swapSuggestion?: Recipe;
  accepted?: boolean;
};

type Day = {
  name: string;
  meals: Meal[];
};

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
                key={meal.recipe.recipe_id}
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
