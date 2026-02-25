"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import StatsCard from "@/components/my-plan/StatsCard";
import DaySelector from "@/components/my-plan/DaySelector";
import DaySection from "@/components/my-plan/DaySection";
import { Droplet, Dumbbell, Flame, Zap } from "lucide-react";
import { useProfile } from "@/hooks/useProfile";
import { useState, useEffect } from "react";

const DAY_NAMES: Record<number, string> = {
  1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday",
  5: "Friday", 6: "Saturday", 7: "Sunday",
};

function getFirstImage(image_url: string | null | undefined): string | undefined {
  if (!image_url) return undefined;
  return image_url.split(/,\s*https?:\/\//)[0].trim() || undefined;
}

function transformPlan(plan: any) {
  if (!plan?.daily_menus) return [];
  return plan.daily_menus
    .sort((a: any, b: any) => a.day_of_week - b.day_of_week)
    .map((menu: any) => ({
      name: DAY_NAMES[menu.day_of_week] ?? `Day ${menu.day_of_week}`,
      meals: (menu.meal_details ?? []).map((detail: any) => ({
        title: detail.recipe?.name ?? "Unknown recipe",
        calories: detail.recipe?.calories ?? 0,
        description: detail.meal_type ?? "",
        image: getFirstImage(detail.recipe?.image_url),
      })),
    }));
}

export default function MyPlanPage() {
  const { profile } = useProfile();
  const [weekData, setWeekData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
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
        <div className="py-12 text-center text-muted-foreground">No plan found. Generate one from the chat!</div>
      ) : (
        <>
          <DaySelector days={weekData} />
          <div className="flex flex-col gap-10">
            {weekData.map((day) => (
              <DaySection key={day.name} day={day} />
            ))}
          </div>
        </>
      )}

      <DaySelector days={weekData} />

      {/* Days */}
      <div className="flex flex-col gap-10">
        {weekData.map((day) => (
          <DaySection key={day.name} day={day} />
        ))}
      </div>
    </AppLayout>
  );
}
