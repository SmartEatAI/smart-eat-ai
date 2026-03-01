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
import { PlanResponse, RecipeResponse, UIDayPlan } from "@/types/my-plan";

const DAY_NAMES: Record<number, string> = {
  1: "Monday",
  2: "Tuesday",
  3: "Wednesday",
  4: "Thursday",
  5: "Friday",
  6: "Saturday",
  7: "Sunday",
};

export function transformPlan(plan: PlanResponse | null): UIDayPlan[] {
  if (!plan?.daily_menus) return [];

  return [...plan.daily_menus]
    .sort((a, b) => a.day_of_week - b.day_of_week)
    .map((menu) => ({
      id: menu.id,
      day_of_week: menu.day_of_week,
      name: DAY_NAMES[menu.day_of_week] ?? `Day ${menu.day_of_week}`,
      meals: [...menu.meal_details].sort(
        (a, b) => a.schedule - b.schedule
      ),
    }));
}

export default function MyPlanPage() {
  const { token } = useAuth();

  const { profile } = useProfile();
  const [weekData, setWeekData] = useState<UIDayPlan[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/plan/current", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.ok ? res.json() : null)
      .then((data) => setWeekData(transformPlan(data)))
      .catch(() => setWeekData([]))
      .finally(() => setLoading(false));
  }, []);

  async function fetchNewRecipe(mealType: string, recipeId: number) {
    try {
      const response = await fetch(
        `http://localhost:8000/api/ml/swap-recipe?recipe_id=${recipeId}&meal_label=${mealType}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log("Swap recipe response status:", response);

      if (!response.ok) throw new Error("Swap recipe failed");

      const data = await response.json();
      return data as RecipeResponse; // asegurarte que backend devuelve la receta completa
    } catch (err) {
      console.error(err);
      return null;
    }
  }

  async function updateMealRecipe(mealDetailId: number, newRecipeId: number) {
    const response = await fetch(
      `http://localhost:8000/api/meal-detail/${mealDetailId}?recipe_id=${newRecipeId}`,
      {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error("Failed to update meal detail");
    }

    return await response.json();
  }

  async function handleConfirmSwap(
    mealDetailId: number,
    newRecipe: RecipeResponse
  ) {
    await updateMealRecipe(mealDetailId, newRecipe.recipe_id);

    setWeekData((prev) =>
      prev.map((day) => ({
        ...day,
        meals: day.meals.map((meal) =>
          meal.id === mealDetailId
            ? { ...meal, recipe: newRecipe }
            : meal
        ),
      }))
    );
  }

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
        // Use recipe fields for macro calculation
        dayCalories += meal.recipe?.calories || 0;
        dayProtein += meal.recipe?.protein || 0;
        dayCarbs += meal.recipe?.carbs || 0;
        dayFats += meal.recipe?.fat || 0;
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
                onConfirmSwap={handleConfirmSwap}
                fetchNewRecipe={fetchNewRecipe}
              />
            ))}
          </div>
        </>
      )}
    </AppLayout>
  );
}