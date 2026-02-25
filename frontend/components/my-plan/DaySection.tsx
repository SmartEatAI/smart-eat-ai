import MealItem from "./MealItem";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";

type Meal = {
  id?: number;
  recipeId?: number;
  title: string;
  calories: number;
  description: string;
  images?: string[];
};

type Day = {
  name: string;
  meals: Meal[];
};

export default function DaySection({ day }: { day: Day }) {
  return (
    <section id={day.name.toLowerCase()} className="flex flex-col gap-4 scroll-mt-[20vh]">
      <h3 className="text-xl font-bold">
        {day.name}
      </h3>

      <Carousel opts={{ loop: true, align: "start" }} className="w-full">
        <CarouselContent className="-ml-2 md:-ml-4">
          {day.meals.map((meal, i) => (
            <CarouselItem
              key={i}
              className="pl-2 md:pl-4 md:basis-1/2 lg:basis-1/3 min-w-55 max-w-87.5 w-full"
            >
              <MealItem meal={meal} />
            </CarouselItem>
          ))}
        </CarouselContent>
        <CarouselPrevious className="hidden lg:flex left-2" />
        <CarouselNext className="hidden lg:flex right-2" />
      </Carousel>
    </section>
  );
}
