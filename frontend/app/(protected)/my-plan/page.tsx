"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import ProtectedRoute from "@/components/auth/ProtectedRoute";
import StatsCard from "@/components/my-plan/StatsCard";
import DaySelector from "@/components/my-plan/DaySelector";
import DaySection from "@/components/my-plan/DaySection";
import { Droplet, Dumbbell, Flame, Zap } from "lucide-react";


import { useProfile } from "@/hooks/useProfile";

export default function MyPlanPage() {
  const { profile } = useProfile();
  const macros = {
    calories: { current: 0, goal: profile?.calories_target || 0 },
    protein: { current: 0, goal: profile?.protein_target || 0 },
    carbs: { current: 0, goal: profile?.carbs_target || 0 },
    fats: { current: 0, goal: profile?.fat_target || 0 },
  };

  const weekData = [
    {
      name: "Monday",
      meals: [
        {
          title: "Oatmeal with berries",
          calories: 350,
          protein: 10,
          carbs: 60,
          fats: 5,
          description: "Oatmeal with strawberries and chia",
        },
        {
          title: "Quinoa bowl",
          calories: 480,
          protein: 15,
          carbs: 80,
          fats: 8,
          description: "Quinoa with chickpeas",
        },
        {
          title: "Baked salmon",
          calories: 450,
          protein: 35,
          carbs: 5,
          fats: 25,
          description: "Salmon with asparagus",
        },
        {
          title: "Baked salmon",
          calories: 450,
          protein: 35,
          carbs: 5,
          fats: 25,
          description: "Salmon with asparagus",
        },
      ],
    },
    {
      name: "Tuesday",
      meals: [
        {
          title: "Avocado toast",
          calories: 410,
          protein: 8,
          carbs: 45,
          fats: 18,
          description: "Whole wheat bread with avocado",
        },
        {
          title: "Caesar salad",
          calories: 520,
          protein: 30,
          carbs: 10,
          fats: 35,
          description: "Chicken with lettuce",
        },
        {
          title: "Pumpkin cream",
          calories: 350,
          protein: 4,
          carbs: 40,
          fats: 12,
          description: "Pumpkin with coconut",
        }, {
          title: "Pumpkin cream",
          calories: 350,
          protein: 4,
          carbs: 40,
          fats: 12,
          description: "Pumpkin with coconut",
        }, {
          title: "Pumpkin cream",
          calories: 350,
          protein: 4,
          carbs: 40,
          fats: 12,
          description: "Pumpkin with coconut",
        },
      ],
    }, {
      name: "Wednesday",
      meals: [
        {
          title: "Avocado toast",
          calories: 410,
          protein: 8,
          carbs: 45,
          fats: 18,
          description: "Whole wheat bread with avocado",
        },
        {
          title: "Caesar salad",
          calories: 520,
          protein: 30,
          carbs: 10,
          fats: 35,
          description: "Chicken with lettuce",
        },
        {
          title: "Pumpkin cream",
          calories: 350,
          protein: 4,
          carbs: 40,
          fats: 12,
          description: "Pumpkin with coconut",
        },
      ],
    }, {
      name: "Thursday",
      meals: [
        {
          title: "Avocado toast",
          calories: 410,
          protein: 8,
          carbs: 45,
          fats: 18,
          description: "Whole wheat bread with avocado",
        },
        {
          title: "Caesar salad",
          calories: 520,
          protein: 30,
          carbs: 10,
          fats: 35,
          description: "Chicken with lettuce",
        },
        {
          title: "Pumpkin cream",
          calories: 350,
          protein: 4,
          carbs: 40,
          fats: 12,
          description: "Pumpkin with coconut",
        }, {
          title: "Pumpkin cream",
          calories: 350,
          protein: 4,
          carbs: 40,
          fats: 12,
          description: "Pumpkin with coconut",
        }, {
          title: "Pumpkin cream",
          calories: 350,
          protein: 4,
          carbs: 40,
          fats: 12,
          description: "Pumpkin with coconut",
        }, {
          title: "Pumpkin cream",
          calories: 350,
          protein: 4,
          carbs: 40,
          fats: 12,
          description: "Pumpkin with coconut",
        },
      ],
    }, {
      name: "Friday",
      meals: [
        {
          title: "Avocado toast",
          calories: 410,
          protein: 8,
          carbs: 45,
          fats: 18,
          description: "Whole wheat bread with avocado",
        },
        {
          title: "Caesar salad",
          calories: 520,
          protein: 30,
          carbs: 10,
          fats: 35,
          description: "Chicken with lettuce",
        },
        {
          title: "Pumpkin cream",
          calories: 350,
          protein: 4,
          carbs: 40,
          fats: 12,
          description: "Pumpkin with coconut",
        },
      ],
    }, {
      name: "Saturday",
      meals: [
        {
          title: "Avocado toast",
          calories: 410,
          protein: 8,
          carbs: 45,
          fats: 18,
          description: "Whole wheat bread with avocado",
        },
        {
          title: "Caesar salad",
          calories: 520,
          protein: 30,
          carbs: 10,
          fats: 35,
          description: "Chicken with lettuce",
        },
        {
          title: "Pumpkin cream",
          calories: 350,
          protein: 4,
          carbs: 40,
          fats: 12,
          description: "Pumpkin with coconut",
        },
      ],
    }, {
      name: "Sunday",
      meals: [
        {
          title: "Avocado toast",
          calories: 410,
          protein: 8,
          carbs: 45,
          fats: 18,
          description: "Whole wheat bread with avocado",
        },
        {
          title: "Caesar salad",
          calories: 520,
          protein: 30,
          carbs: 10,
          fats: 35,
          description: "Chicken with lettuce",
        },
        {
          title: "Pumpkin cream",
          calories: 350,
          protein: 4,
          carbs: 40,
          fats: 12,
          description: "Pumpkin with coconut",
        },

      ],
    },
  ];

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
