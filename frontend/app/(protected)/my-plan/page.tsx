"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import ProtectedRoute from "@/components/auth/ProtectedRoute";
import StatsCard from "@/components/my-plan/StatsCard";
import DaySelector from "@/components/my-plan/DaySelector";
import DaySection from "@/components/my-plan/DaySection";
import { Droplet, Dumbbell, Flame, Zap  } from "lucide-react";


import { useProfile } from "@/hooks/useProfile";

export default function MyPlanPage() {
  const { profile } = useProfile();
  const macros = {
    calories: { current: 0, goal: profile?.calories_target || 0 },
    protein: { current: 0, goal: profile?.protein_target || 0 },
    carbs: { current: 0, goal: profile?.carbs_target || 0 },
    fats: { current: 0, goal: profile?.fat_target || 0 },
  };

  const stats = [
    {
      title: "Calories",
      current: macros.calories.current,
      goal: macros.calories.goal,
      unit: "kcal",
      icon: <Flame />,
    },
    {
      title: "Proteins",
      current: macros.protein.current,
      goal: macros.protein.goal,
      unit: "g",
      icon: <Dumbbell />,
    },
    {
      title: "Carbohydrates",
      current: macros.carbs.current,
      goal: macros.carbs.goal,
      unit: "g",
      icon: <Zap />,
    },
    {
      title: "Fats",
      current: macros.fats.current,
      goal: macros.fats.goal,
      unit: "g",
      icon: <Droplet />,
    },
  ];

  const weekData = [
    {
      name: "Monday",
      meals: [
        {
          title: "Oatmeal with berries",
          calories: 350,
          description: "Oatmeal with strawberries and chia",
        },
        {
          title: "Quinoa bowl",
          calories: 480,
          description: "Quinoa with chickpeas",
        },
        {
          title: "Baked salmon",
          calories: 450,
          description: "Salmon with asparagus",
        },
        {
          title: "Baked salmon",
          calories: 450,
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
          description: "Whole wheat bread with avocado",
        },
        {
          title: "Caesar salad",
          calories: 520,
          description: "Chicken with lettuce",
        },
        {
          title: "Pumpkin cream",
          calories: 350,
          description: "Pumpkin with coconut",
        },{
          title: "Pumpkin cream",
          calories: 350,
          description: "Pumpkin with coconut",
        },{
          title: "Pumpkin cream",
          calories: 350,
          description: "Pumpkin with coconut",
        },
      ],
    },{
      name: "Wednesday",
      meals: [
        {
          title: "Avocado toast",
          calories: 410,
          description: "Whole wheat bread with avocado",
        },
        {
          title: "Caesar salad",
          calories: 520,
          description: "Chicken with lettuce",
        },
        {
          title: "Pumpkin cream",
          calories: 350,
          description: "Pumpkin with coconut",
        },
      ],
    },{
      name: "Thursday",
      meals: [
        {
          title: "Avocado toast",
          calories: 410,
          description: "Whole wheat bread with avocado",
        },
        {
          title: "Caesar salad",
          calories: 520,
          description: "Chicken with lettuce",
        },
        {
          title: "Pumpkin cream",
          calories: 350,
          description: "Pumpkin with coconut",
        },{
          title: "Pumpkin cream",
          calories: 350,
          description: "Pumpkin with coconut",
        },{
          title: "Pumpkin cream",
          calories: 350,
          description: "Pumpkin with coconut",
        },{
          title: "Pumpkin cream",
          calories: 350,
          description: "Pumpkin with coconut",
        },
      ],
    },{
      name: "Friday",
      meals: [
        {
          title: "Avocado toast",
          calories: 410,
          description: "Whole wheat bread with avocado",
        },
        {
          title: "Caesar salad",
          calories: 520,
          description: "Chicken with lettuce",
        },
        {
          title: "Pumpkin cream",
          calories: 350,
          description: "Pumpkin with coconut",
        },
      ],
    },{
      name: "Saturday",
      meals: [
        {
          title: "Avocado toast",
          calories: 410,
          description: "Whole wheat bread with avocado",
        },
        {
          title: "Caesar salad",
          calories: 520,
          description: "Chicken with lettuce",
        },
        {
          title: "Pumpkin cream",
          calories: 350,
          description: "Pumpkin with coconut",
        },
      ],
    },{
      name: "Sunday",
      meals: [
        {
          title: "Avocado toast",
          calories: 410,
          description: "Whole wheat bread with avocado",
        },
        {
          title: "Caesar salad",
          calories: 520,
          description: "Chicken with lettuce",
        },
        {
          title: "Pumpkin cream",
          calories: 350,
          description: "Pumpkin with coconut",
        },
      ],
    },
  ];


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
