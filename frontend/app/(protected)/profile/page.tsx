"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import { useEffect, useState } from "react";
import { useProfile } from "@/hooks/useProfile";
import BiometricsSection from "@/components/profile/BiometricsSection";
import GoalSection from "@/components/profile/GoalSection";
import PreferencesSection from "@/components/profile/PreferencesSection";
import Button from "@/components/ui/Button";
import Toast from "@/components/ui/Toast";


export default function ProfilePage() {
  const { profile, loading, error, updateProfile } = useProfile();
  const [form, setForm] = useState<any | null>(null);
  const [toast, setToast] = useState<{ message: string; type: "success" | "error" } | null>(null);

  // Estados para las opciones de la API
  const [availableRestrictions, setAvailableRestrictions] = useState<string[]>([]);
  const [availableTastes, setAvailableTastes] = useState<string[]>([]);

  const fetchOptions = async () => {
  try {
      const [restrRes, tastesRes] = await Promise.all([
        fetch("http://localhost:8000/api/restriction"),
        fetch("http://localhost:8000/api/taste")
      ]);
      const restrData = await restrRes.json();
      const tastesData = await tastesRes.json();

      setAvailableRestrictions(restrData.map((i: any) => typeof i === 'string' ? i : i.name));
      setAvailableTastes(tastesData.map((i: any) => typeof i === 'string' ? i : i.name));
    } catch (err) {
      console.error("Error fetching options:", err);
    }
  };
  
  useEffect(() => {
    fetchOptions();
  }, []);

  useEffect(() => {
    if (profile) {
      setForm({ ...profile });
    } else {
      setForm({
        birth_date: null,
        age: null,
        goal: null,
        activity_level: null,
        meals_per_day: null,
        diet_types: [],    // Puede estar vacío inicialmente
        restrictions: [],  // Puede estar vacío inicialmente
        tastes: [],        // Puede estar vacío inicialmente
      });
    }
  }, [profile]);


  // Helper para actualizar birth_date a partir de age
  const updateField = (field: string, value: any) => {
    if (!form) return;
    if (field === "age") {
      if (value === null || value === undefined || value === "") {
        setForm((prev: any) => ({ ...prev, age: null, birth_date: null }));
      } else {
        // Calcular birth_date a partir de la edad
        const today = new Date();
        const birthYear = today.getFullYear() - value;
        const birthDate = new Date(birthYear, today.getMonth(), today.getDate());
        setForm((prev: any) => ({ ...prev, age: value, birth_date: birthDate.toISOString().split("T")[0] }));
      }
    } else {
      setForm((prev: any) => ({ ...prev, [field]: value }));
    }
  };

  // Helper para obtener la edad desde birth_date
  const getAge = () => {
    if (!form?.birth_date) return "";
    const birth = new Date(form.birth_date);
    if (isNaN(birth.getTime())) return "";
    const today = new Date();
    let age = today.getFullYear() - birth.getFullYear();
    const m = today.getMonth() - birth.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    return age;
  };


  const [birthDateError, setBirthDateError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<any>({});

  function isValidBirthDate(dateStr: string | null) {
    if (!dateStr) return true; // Permitir nulo para crear perfil
    const birth = new Date(dateStr);
    if (isNaN(birth.getTime())) return false;
    const today = new Date();
    let age = today.getFullYear() - birth.getFullYear();
    const m = today.getMonth() - birth.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    return age >= 16 && age <= 100;
  }

  const validateFields = () => {
    const errors: any = {};
    // Goal
    if (!form.goal) {
      errors.goal = "Goal is required";
    }
    // Height
    if (form.height === null || form.height === undefined || form.height === "") {
      errors.height = "Height is required";
    } else if (isNaN(Number(form.height)) || Number(form.height) < 140 || Number(form.height) > 220) {
      errors.height = "Height must be between 140 and 220 cm";
    }
    // Weight
    if (form.weight === null || form.weight === undefined || form.weight === "") {
      errors.weight = "Weight is required";
    } else if (isNaN(Number(form.weight)) || Number(form.weight) < 35 || Number(form.weight) > 300) {
      errors.weight = "Weight must be between 35 and 300 kg";
    }
    // Body type
    if (!form.body_type) {
      errors.body_type = "Body type is required";
    }
    // Gender
    if (!form.gender) {
      errors.gender = "Gender is required";
    }
    // Meals per day
    if (form.meals_per_day === null || form.meals_per_day === undefined || form.meals_per_day === "") {
      errors.meals_per_day = "Meals per day is required";
    } else if (isNaN(Number(form.meals_per_day)) || Number(form.meals_per_day) < 1 || Number(form.meals_per_day) > 6) {
      errors.meals_per_day = "Meals per day must be between 1 and 6";
    }
    // Activity level
    if (!form.activity_level) {
      errors.activity_level = "Activity level is required";
    }
    // Birth date / Age
    if (!form.age && !form.birth_date) {
      errors.age = "Age or birth date is required";
    } else if (form.birth_date && !isValidBirthDate(form.birth_date)) {
      errors.birth_date = "The birth date must indicate an age between 16 and 100 years.";
    }
    // Opcionales pero deben ser numéricos >= 0 si se proveen
    if (form.body_fat_percentage !== undefined && form.body_fat_percentage !== null && form.body_fat_percentage !== "") {
      if (isNaN(Number(form.body_fat_percentage)) || Number(form.body_fat_percentage) < 0) {
        errors.body_fat_percentage = "Body fat % must be 0 or greater";
      }
    }
    if (form.calories_target !== undefined && form.calories_target !== null && form.calories_target !== "") {
      if (isNaN(Number(form.calories_target)) || Number(form.calories_target) < 0) {
        errors.calories_target = "Calories target must be 0 or greater";
      }
    }
    if (form.protein_target !== undefined && form.protein_target !== null && form.protein_target !== "") {
      if (isNaN(Number(form.protein_target)) || Number(form.protein_target) < 0) {
        errors.protein_target = "Protein target must be 0 or greater";
      }
    }
    if (form.carbs_target !== undefined && form.carbs_target !== null && form.carbs_target !== "") {
      if (isNaN(Number(form.carbs_target)) || Number(form.carbs_target) < 0) {
        errors.carbs_target = "Carbs target must be 0 or greater";
      }
    }
    if (form.fat_target !== undefined && form.fat_target !== null && form.fat_target !== "") {
      if (isNaN(Number(form.fat_target)) || Number(form.fat_target) < 0) {
        errors.fat_target = "Fat target must be 0 or greater";
      }
    }
    // Los arrays pueden ir vacíos, no validar diet_types, restrictions, tastes
    return errors;
  };

  const saveProfile = async () => {
    if (!form) return;
    const errors = validateFields();
    setFieldErrors(errors);
    if (Object.keys(errors).length > 0) {
      setToast({ message: "Please fill all required fields.", type: "error" });
      return;
    }
    // Normalizar birth_date a YYYY-MM-DD o null
    let birth_date = form.birth_date;
    if (birth_date instanceof Date) {
      birth_date = birth_date.toISOString().split("T")[0];
    }
    if (birth_date === "" || birth_date === undefined) birth_date = null;
    if (!isValidBirthDate(birth_date)) {
      setBirthDateError("The birth date must indicate an age between 16 and 100 years.");
      return;
    }
    setBirthDateError(null);
    try {
      await updateProfile({ ...form, birth_date });
      await fetchOptions();
      setToast({
        message: "Profile saved!",
        type: "success"
      });
    } catch (error: any) {
      setToast({
        message: error?.message || "Error saving profile.",
        type: "error"
      });
    }
  };


  if (loading) return <div className="p-8">Loading page profile...</div>;
  if (error) return <div className="p-8 text-red-500">{error}</div>;
  if (!form) return null;

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
                {/* Errores de biometría */}
                {fieldErrors.height && (<div className="text-red-500 text-sm mt-2">{fieldErrors.height}</div>)}
                {fieldErrors.weight && (<div className="text-red-500 text-sm mt-2">{fieldErrors.weight}</div>)}
                {fieldErrors.body_type && (<div className="text-red-500 text-sm mt-2">{fieldErrors.body_type}</div>)}
                {fieldErrors.gender && (<div className="text-red-500 text-sm mt-2">{fieldErrors.gender}</div>)}
                {fieldErrors.age && (<div className="text-red-500 text-sm mt-2">{fieldErrors.age}</div>)}
                {fieldErrors.birth_date && (<div className="text-red-500 text-sm mt-2">{fieldErrors.birth_date}</div>)}
                {fieldErrors.body_fat_percentage && (<div className="text-red-500 text-sm mt-2">{fieldErrors.body_fat_percentage}</div>)}
                {fieldErrors.calories_target && (<div className="text-red-500 text-sm mt-2">{fieldErrors.calories_target}</div>)}
                {fieldErrors.protein_target && (<div className="text-red-500 text-sm mt-2">{fieldErrors.protein_target}</div>)}
                {fieldErrors.carbs_target && (<div className="text-red-500 text-sm mt-2">{fieldErrors.carbs_target}</div>)}
                {fieldErrors.fat_target && (<div className="text-red-500 text-sm mt-2">{fieldErrors.fat_target}</div>)}
                {birthDateError && (<div className="text-red-500 text-sm mt-2">{birthDateError}</div>)}
              </div>
              <div className="bg-card rounded-xl shadow p-6">
                <h2 className="text-xl font-bold mb-2">Goal</h2>
                <p className="text-muted-foreground mb-4">Set your nutrition and activity goals.</p>
                <GoalSection
                  goal={form.goal ?? null}
                  setGoal={(g) => updateField("goal", g)}
                  activityLevel={form.activity_level ?? null}
                  setActivityLevel={(v) => updateField("activity_level", v)}
                />
                {/* Errores de goal y activity_level */}
                {fieldErrors.goal && (
                  <div className="text-red-500 text-sm mt-2">{fieldErrors.goal}</div>
                )}
                {fieldErrors.activity_level && (
                  <div className="text-red-500 text-sm mt-2">{fieldErrors.activity_level}</div>
                )}
              </div>
            </div>

            <div className="lg:col-span-4 flex flex-col gap-5 h-full">
              <div className="bg-card rounded-xl shadow p-6 h-full flex-1 flex flex-col">
                <h2 className="text-xl font-bold mb-2">Preferences</h2>
                <p className="text-muted-foreground mb-4">Customize your dietary preferences.</p>
                <PreferencesSection
                  meals={form.meals_per_day ?? null}
                  setMeals={(n) => updateField("meals_per_day", n)}
                  dietTypes={form.diet_types || []}
                  setDietTypes={(diets) => updateField("diet_types", diets)}
                  restrictions={form.restrictions || []}
                  setRestrictions={(r) => updateField("restrictions", r)}
                  tastes={form.tastes || []}
                  setTastes={(t) => updateField("tastes", t)}
                  availableRestrictions={availableRestrictions}
                  availableTastes={availableTastes}
                />
                {/* Errores de preferencias */}
                {fieldErrors.meals_per_day && (
                  <div className="text-red-500 text-sm mt-2">{fieldErrors.meals_per_day}</div>
                )}
              </div>
              <Button onClick={saveProfile}>
                Save Profile
              </Button>
            </div>
          </div>
        </div>
        {/* Toast Notification */}
        {toast && (
          <Toast
            message={toast.message}
            type={toast.type}
            onClose={() => setToast(null)}
          />
        )}
      </div>
    </AppLayout>
  );
}
