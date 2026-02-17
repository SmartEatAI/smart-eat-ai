"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import { useState } from "react";
import Sidebar from "@/components/layout/Sidebar";
import BiometricsSection from "@/components/profile/BiometricsSection";
import GoalSection from "@/components/profile/GoalSection";
import PreferencesSection from "@/components/profile/PreferencesSection";
import Button from "@/components/ui/Button";

export default function ProfilePage() {
  const [form, setForm] = useState({
    age: 30,
    weight: 75,
    height: 175,
    goal: "maintain",
    meals: 4,
  });

  const updateField = (field: string, value: any) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const saveProfile = () => {
    console.log("Perfil guardado:", form);
  };

  return (
    <AppLayout
      title="⚙️ Configuración Nutricional"
      subtitle="Ayúdanos a calibrar tu Chef Personal Inteligente para obtener mejores resultados."
    >
      <div className="flex flex-col h-[80vh]">
        {/* Zona de configuracion */}
        <div className="flex-1 flex flex-col gap-4 p-4">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <div className="lg:col-span-8 flex flex-col gap-8">
              <BiometricsSection
                data={form}
                onChange={updateField}
              />

              <GoalSection
                goal={form.goal}
                setGoal={(g) => updateField("goal", g)}
              />
            </div>
          

          <div className="lg:col-span-4 flex flex-col gap-8">
            <PreferencesSection
              meals={form.meals}
              setMeals={(n) => updateField("meals", n)}
            />

            <Button onClick={saveProfile}>
              Guardar Perfil
            </Button>
          </div>
          </div>
        </div>

      </div>
    </AppLayout>
  );
}