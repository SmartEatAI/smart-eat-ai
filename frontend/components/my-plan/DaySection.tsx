import { RecipeResponse, UIDayPlan } from "@/types/my-plan";
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from "../ui/carousel";
import MealItemTest from "./MealItemTest";

export default function DaySection({
  day,
  dayIndex,
  onConfirmSwap,
  fetchNewRecipe,
}: {
  day: UIDayPlan;
  dayIndex: number;
  onConfirmSwap: (mealDetailId: number, newRecipe: RecipeResponse) => Promise<void>;
  fetchNewRecipe: (mealType: string, recipeId: number) => Promise<RecipeResponse | null>;
}) {
  return (
    <section
      id={day.name.toLowerCase()}
      className="flex flex-col gap-4 scroll-mt-[20vh]"
    >
      <h3 className="text-xl font-bold">
        {day.name}
      </h3>

      <Carousel opts={{ loop: true, align: "start" }} className="w-full">
        <CarouselContent className="-ml-2 md:-ml-4">
          {day.meals.map((meal, mealIndex) =>
            meal.recipe ? (
              <CarouselItem
                key={`meal-${dayIndex}-${mealIndex}-${meal.id}`}
                className="pl-2 md:pl-4 md:basis-1/2 lg:basis-1/3 min-w-[220px] max-w-[350px] w-full"
              >
                <MealItemTest
                  meal={meal}
                  mealDetailId={meal.id}
                  swappable={true}
                  onConfirmSwap={onConfirmSwap}
                  fetchNewRecipe={fetchNewRecipe}
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