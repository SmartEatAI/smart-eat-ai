"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import StatsCard from "@/components/my-plan/StatsCard";
import DaySelector from "@/components/my-plan/DaySelector";
import DaySection from "@/components/my-plan/DaySection";
import { Droplet, Dumbbell, Flame, Zap } from "lucide-react";
import { useProfile } from "@/hooks/useProfile";
import { useState, useEffect } from "react";
import { useAuth } from "@/hooks/useAuth";
import NoPlanCard from "@/components/my-plan/NoPlanCard";

const DAY_NAMES: Record<number, string> = {
  1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday",
  5: "Friday", 6: "Saturday", 7: "Sunday",
};

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

function getFirstImage(image_url: string | null | undefined): string | undefined {
  if (!image_url) return undefined;
  return image_url.split(/,\s*https?:\/\//)[0].trim() || undefined;
}

function transformPlan(plan: any): DayPlan[] {
  if (!plan?.daily_menus) return [];
  return plan.daily_menus
    .sort((a: any, b: any) => a.day_of_week - b.day_of_week)
    .map((menu: any): DayPlan => ({
      name: DAY_NAMES[menu.day_of_week] ?? `Day ${menu.day_of_week}`,
      meals: (menu.meal_details ?? []).map((detail: any): MealItem => {
        const recipeData = detail.recipe ?? {};
        const recipe: Recipe = {
          recipe_id: recipeData.recipe_id ?? 0,
          name: recipeData.name ?? "Unknown recipe",
          image_url: recipeData.image_url ?? "",
          calories: recipeData.calories ?? 0,
          protein: recipeData.protein ?? 0,
          carbs: recipeData.carbs ?? 0,
          fat: recipeData.fat ?? 0,
          meal_types: recipeData.meal_types ?? [],
          diet_types: recipeData.diet_types ?? [],
          recipe_url: recipeData.recipe_url ?? "",
        };

        return {
          recipe,
          meal_type: detail.meal_type ?? "",
          swapSuggestion: undefined,
          accepted: false,
        };
      }),
    }));
}

export default function MyPlanPage() {
  const { user, token } = useAuth();

  const { profile } = useProfile();
  const [weekData, setWeekData] = useState<DayPlan[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [loading, setLoading] = useState(true);

  async function fetchNewRecipe(mealType: string, recipeId: number) {
    try {
      const response = await fetch(`http://localhost:8000/api/ml/swap-recipe?recipe_id=${recipeId}&meal_label=${mealType}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );
      const data = await response.json();
      return data; // Debería contener la nueva receta sugerida
    } catch (error) {
      console.error("Error fetching new recipe:", error);
    }
  }

  const handleSwapMeal = async (dayIndex: number, mealIndex: number) => {
    const meal = weekData[dayIndex].meals[mealIndex];
    // Llamada a tu API para obtener nueva sugerencia
    const mealType = Array.isArray(meal.meal_type)
      ? meal.meal_type[0]
      : meal.meal_type;
    const newSwap = await fetchNewRecipe(mealType, meal.recipe.recipe_id);
    if (!newSwap) return;

    // Actualiza estado local
    setWeekData(prev => {
      const updated = [...prev];
      updated[dayIndex].meals[mealIndex].swapSuggestion = newSwap;
      updated[dayIndex].meals[mealIndex].accepted = false;
      return updated;
    });
  };

  const handleAcceptSwap = (dayIndex: number, mealIndex: number) => {
    setWeekData(prev => {
      const updated = [...prev];
      const meal = updated[dayIndex].meals[mealIndex];
      if (meal.swapSuggestion) {
        meal.recipe = meal.swapSuggestion; // reemplaza la receta
        meal.swapSuggestion = undefined;   // borra sugerencia
        meal.accepted = true;
      }
      return updated;
    });
  };

  useEffect(() => {
    fetch("http://localhost:8000/api/plan/current", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.ok ? res.json() : null)
      .then((data) => setWeekData(transformPlan(data)))
      .catch(() => setWeekData([]))
      .finally(() => setLoading(false));
  }, []);

  const macros = {
    calories: { current: 0, goal: profile?.calories_target || 0 },
    protein: { current: 0, goal: profile?.protein_target || 0 },
    carbs: { current: 0, goal: profile?.carbs_target || 0 },
    fats: { current: 0, goal: profile?.fat_target || 0 },
  };

  const promedioMacros = calcularPromedioMacros(weekData);

  const stats = [
    {
      title: "Calories",
      current: Number(promedioMacros.calories.toFixed(1)),
      goal: macros.calories.goal,
      unit: "kcal",
      icon: <Flame />,
    },
    {
      title: "Proteins",
      current: Number(promedioMacros.protein.toFixed(1)),
      goal: macros.protein.goal,
      unit: "g",
      icon: <Dumbbell />,
    },
    {
      title: "Carbohydrates",
      current: Number(promedioMacros.carbs.toFixed(1)),
      goal: macros.carbs.goal,
      unit: "g",
      icon: <Zap />,
    },
    {
      title: "Fats",
      current: Number(promedioMacros.fats.toFixed(1)),
      goal: macros.fats.goal,
      unit: "g",
      icon: <Droplet />,
    },
  ];

  // Función para calcular el promedio semanal de macros
  function calcularPromedioMacros(weekData: any[]) {
    let totalCalories = 0, totalProtein = 0, totalCarbs = 0, totalFats = 0;
    const numDias = weekData.length;
    weekData.forEach(day => {
      let dayCalories = 0, dayProtein = 0, dayCarbs = 0, dayFats = 0;
      day.meals.forEach((meal: any) => {
        dayCalories += meal.calories || 0;
        dayProtein += meal.protein || 0;
        dayCarbs += meal.carbs || 0;
        dayFats += meal.fats || 0;
      });
      totalCalories += dayCalories;
      totalProtein += dayProtein;
      totalCarbs += dayCarbs;
      totalFats += dayFats;
    });
    return {
      calories: numDias ? totalCalories / numDias : 0,
      protein: numDias ? totalProtein / numDias : 0,
      carbs: numDias ? totalCarbs / numDias : 0,
      fats: numDias ? totalFats / numDias : 0,
    };
  }

  return (
    <AppLayout
      title="📆 My Nutrition Plan"
      subtitle="Your personalized plan"
    >
      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((item) => (
          <StatsCard key={item.title} {...item} />
        ))}
      </div>

      {loading ? (
        <div className="py-12 text-center text-muted-foreground">Loading plan...</div>
      ) : weekData.length === 0 ? (
        <NoPlanCard />
      ) : (
        <>
          <DaySelector days={weekData} />
          <div className="flex flex-col gap-10">
            {weekData.map((day, dayIndex) => (
              <DaySection
                key={day.name}
                day={day}
                dayIndex={dayIndex}
                onSwapMeal={handleSwapMeal}
                onAcceptSwap={handleAcceptSwap}
              />
            ))}
          </div>
        </>
      )}
    </AppLayout>
  );
}