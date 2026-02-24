"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import ProtectedRoute from "@/components/auth/ProtectedRoute";
import { useEffect, useState } from "react";
import { useProfile } from "@/hooks/useProfile";
import BiometricsSection from "@/components/profile/BiometricsSection";
import GoalSection from "@/components/profile/GoalSection";
import PreferencesSection from "@/components/profile/PreferencesSection";
import Button from "@/components/ui/Button";


function ProfilePage() {
  const { profile, loading, error, updateProfile } = useProfile();
  const [form, setForm] = useState<any>(null);
  useEffect(() => {
    if (profile) {
      setForm({ ...profile });
    }
  }, [profile]);


  // Helper para actualizar birth_date a partir de age
  const updateField = (field: string, value: any) => {
    if (field === "age") {
      // Calcular birth_date a partir de la edad
      const today = new Date();
      const birthYear = today.getFullYear() - value;
      const birthDate = new Date(birthYear, today.getMonth(), today.getDate());
      setForm((prev: any) => ({ ...prev, birth_date: birthDate.toISOString().split("T")[0] }));
    } else {
      setForm((prev: any) => ({ ...prev, [field]: value }));
    }
  };

  // Helper para obtener la edad desde birth_date
  const getAge = () => {
    if (!form?.birth_date) return "";
    const birth = new Date(form.birth_date);
    const today = new Date();
    let age = today.getFullYear() - birth.getFullYear();
    const m = today.getMonth() - birth.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    return age;
  };


  const [birthDateError, setBirthDateError] = useState<string | null>(null);

  function isValidBirthDate(dateStr: string) {
    if (!dateStr) return false;
    const birth = new Date(dateStr);
    const today = new Date();
    let age = today.getFullYear() - birth.getFullYear();
    const m = today.getMonth() - birth.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    return age >= 16 && age <= 100;
  }

  const saveProfile = async () => {
    if (!form) return;
    // Normalizar birth_date a YYYY-MM-DD
    let birth_date = form.birth_date;
    if (birth_date instanceof Date) {
      birth_date = birth_date.toISOString().split("T")[0];
    }
    if (!isValidBirthDate(birth_date)) {
      setBirthDateError("La fecha de nacimiento debe indicar una edad entre 16 y 100 años.");
      return;
    }
    setBirthDateError(null);
    await updateProfile({ ...form, birth_date });
  };


  if (loading || !form) return <div className="p-8">Loading...</div>;
  if (error) return <div className="p-8 text-red-500">{error}</div>;

  return (
    <AppLayout
      title="⚙️ Nutrition Settings"
      subtitle="Help us calibrate your Intelligent Personal Chef for better results."
    >
      <div className="flex flex-col h-[80vh]">
        {/* Zona de configuracion */}
        <div className="flex-1 flex flex-col gap-4 p-4">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <div className="lg:col-span-8 flex flex-col gap-8">
              <div className="bg-card rounded-xl shadow p-6">
                <h2 className="text-xl font-bold mb-2">Biometrics</h2>
                <p className="text-muted-foreground mb-4">Your basic physical information.</p>
                <BiometricsSection
                  data={form}
                  onChange={updateField}
                />
                {birthDateError && (
                  <div className="text-red-500 text-sm mt-2">{birthDateError}</div>
                )}
              </div>
              <div className="bg-card rounded-xl shadow p-6">
                <h2 className="text-xl font-bold mb-2">Goal</h2>
                <p className="text-muted-foreground mb-4">Set your nutrition and activity goals.</p>
                <GoalSection
                  goal={form.goal}
                  setGoal={(g) => updateField("goal", g)}
                  activityLevel={form.activity_level}
                  setActivityLevel={(v) => updateField("activity_level", v)}
                />
              </div>
            </div>

            <div className="lg:col-span-4 flex flex-col gap-5 h-full">
              <div className="bg-card rounded-xl shadow p-6 h-full flex-1 flex flex-col">
                <h2 className="text-xl font-bold mb-2">Preferences</h2>
                <p className="text-muted-foreground mb-4">Customize your dietary preferences.</p>
                <PreferencesSection
                  meals={form.meals_per_day}
                  setMeals={(n) => updateField("meals_per_day", n)}
                  dietTypes={form.diet_types || []}
                  setDietTypes={(diets) => updateField("diet_types", diets)}
                />
              </div>
              <Button onClick={saveProfile}>
                Save Profile
              </Button>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}

export default function ProfilePageWrapper() {
  return (
    <ProtectedRoute>
      <ProfilePage />
    </ProtectedRoute>
  );
}