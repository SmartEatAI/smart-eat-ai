"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import ProtectedRoute from "@/components/auth/ProtectedRoute";
import StatsCard from "@/components/my-plan/StatsCard";
import DaySelector from "@/components/my-plan/DaySelector";
import DaySection from "@/components/my-plan/DaySection";
import { Droplet, Dumbbell, Flame, Zap  } from "lucide-react";

function MyPlanPage() {
  const stats = [
    { title: "Promedio Calórico", value: "1950/2050", unit: "kcal", icon: <Flame /> },
    { title: "Proteínas", value: "135/130", unit: "g", icon: <Dumbbell /> },
    { title: "Carbohidratos", value: "210/250", unit: "g", icon: <Zap /> },
    { title: "Grasas", value: "60/70", unit: "g", icon: <Droplet/> },
  ];

  const weekData = [
    {
      name: "Lunes",
      meals: [
        {
          title: "Avena con frutos rojos",
          calories: 350,
          description: "Avena con fresas y chía",
        },
        {
          title: "Bowl de quinoa",
          calories: 480,
          description: "Quinoa con garbanzos",
        },
        {
          title: "Salmón al horno",
          calories: 450,
          description: "Salmón con espárragos",
        },
        {
          title: "Salmón al horno",
          calories: 450,
          description: "Salmón con espárragos",
        },
      ],
    },
    {
      name: "Martes",
      meals: [
        {
          title: "Tostadas de aguacate",
          calories: 410,
          description: "Pan integral con aguacate",
        },
        {
          title: "Ensalada César",
          calories: 520,
          description: "Pollo con lechuga",
        },
        {
          title: "Crema de calabaza",
          calories: 350,
          description: "Calabaza con coco",
        },{
          title: "Crema de calabaza",
          calories: 350,
          description: "Calabaza con coco",
        },{
          title: "Crema de calabaza",
          calories: 350,
          description: "Calabaza con coco",
        },
      ],
    },{
      name: "Miércoles",
      meals: [
        {
          title: "Tostadas de aguacate",
          calories: 410,
          description: "Pan integral con aguacate",
        },
        {
          title: "Ensalada César",
          calories: 520,
          description: "Pollo con lechuga",
        },
        {
          title: "Crema de calabaza",
          calories: 350,
          description: "Calabaza con coco",
        },
      ],
    },{
      name: "Jueves",
      meals: [
        {
          title: "Tostadas de aguacate",
          calories: 410,
          description: "Pan integral con aguacate",
        },
        {
          title: "Ensalada César",
          calories: 520,
          description: "Pollo con lechuga",
        },
        {
          title: "Crema de calabaza",
          calories: 350,
          description: "Calabaza con coco",
        },{
          title: "Crema de calabaza",
          calories: 350,
          description: "Calabaza con coco",
        },{
          title: "Crema de calabaza",
          calories: 350,
          description: "Calabaza con coco",
        },{
          title: "Crema de calabaza",
          calories: 350,
          description: "Calabaza con coco",
        },
      ],
    },{
      name: "Viernes",
      meals: [
        {
          title: "Tostadas de aguacate",
          calories: 410,
          description: "Pan integral con aguacate",
        },
        {
          title: "Ensalada César",
          calories: 520,
          description: "Pollo con lechuga",
        },
        {
          title: "Crema de calabaza",
          calories: 350,
          description: "Calabaza con coco",
        },
      ],
    },{
      name: "Sabado",
      meals: [
        {
          title: "Tostadas de aguacate",
          calories: 410,
          description: "Pan integral con aguacate",
        },
        {
          title: "Ensalada César",
          calories: 520,
          description: "Pollo con lechuga",
        },
        {
          title: "Crema de calabaza",
          calories: 350,
          description: "Calabaza con coco",
        },
      ],
    },{
      name: "Domingo",
      meals: [
        {
          title: "Tostadas de aguacate",
          calories: 410,
          description: "Pan integral con aguacate",
        },
        {
          title: "Ensalada César",
          calories: 520,
          description: "Pollo con lechuga",
        },
        {
          title: "Crema de calabaza",
          calories: 350,
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