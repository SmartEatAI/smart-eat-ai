"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import ProtectedRoute from "@/components/auth/ProtectedRoute";
import StatsCard from "@/components/my-plan/StatsCard";
import DaySelector from "@/components/my-plan/DaySelector";
import DaySection from "@/components/my-plan/DaySection";
import { Droplet, Dumbbell, Flame, Zap  } from "lucide-react";

function MyPlanPage() {
  const stats = [
    { title: "Average Calories", value: "1950/2050", unit: "kcal", icon: <Flame /> },
    { title: "Proteins", value: "135/130", unit: "g", icon: <Dumbbell /> },
    { title: "Carbohydrates", value: "210/250", unit: "g", icon: <Zap /> },
    { title: "Fats", value: "60/70", unit: "g", icon: <Droplet/> },
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
      title="My Nutrition Plan"
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

export default function MyPlanPageWrapper() {
  return (
    <ProtectedRoute>
      <MyPlanPage />
    </ProtectedRoute>
  );
}