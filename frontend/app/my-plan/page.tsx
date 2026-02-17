"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import StatsCard from "@/components/my-plan/StatsCard";
import DaySelector from "@/components/my-plan/DaySelector";
import DaySection from "@/components/my-plan/DaySection";

export default function MyPlanPage() {
  const stats = [
    { title: "Promedio Calórico", value: "1950", unit: "kcal" },
    { title: "Proteínas", value: "135g" },
    { title: "Carbohidratos", value: "210g" },
    { title: "Grasas", value: "60g" },
  ];

  const weekData = [
    {
      name: "Lunes",
      date: 23,
      meals: [
        {
          title: "Avena con frutos rojos",
          kcal: 350,
          description: "Avena con fresas y chía",
        },
        {
          title: "Bowl de quinoa",
          kcal: 480,
          description: "Quinoa con garbanzos",
        },
        {
          title: "Salmón al horno",
          kcal: 450,
          description: "Salmón con espárragos",
        },
      ],
    },
    {
      name: "Martes",
      date: 24,
      meals: [
        {
          title: "Tostadas de aguacate",
          kcal: 410,
          description: "Pan integral con aguacate",
        },
        {
          title: "Ensalada César",
          kcal: 520,
          description: "Pollo con lechuga",
        },
        {
          title: "Crema de calabaza",
          kcal: 350,
          description: "Calabaza con coco",
        },
      ],
    },
  ];


  return (
    <AppLayout
      title="Mi Plan Nutricional"
      subtitle="Tu plan personalizado"
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
          <DaySection key={day.date} day={day} />
        ))}
      </div>
    </AppLayout>
  );
}