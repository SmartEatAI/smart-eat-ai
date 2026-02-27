import { Category } from "./category";

export type Recipe = {
  recipe_id: number;
  name: string;
  image_url: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  meal_types: string[];
  diet_types: string[];
  recipe_url: string;
};

export type MealItem = {
  recipe: Recipe;
  meal_type: string;
  swapSuggestion?: Recipe; // alternativa sugerida por swap
  accepted?: boolean; // si el usuario aceptó la sugerencia
};

export type DayPlan = {
  name: string;
  meals: MealItem[];
};

export type StatsCardProps = {
  title: string;
  current: number | string;
  goal: number | string;
  unit?: string;
  bgColor?: string;
  icon?: React.ReactNode;
};

export type BiometricsSectionProps = {
  data: any;
  onChange: (field: string, value: any) => void;
};

export type GoalSectionProps = {
  goal: string;
  setGoal: (goal: string) => void;
  activityLevel: string;
  setActivityLevel: (level: string) => void;
};

export type PreferencesSectionProps = {
  meals: number;
  setMeals: (n: number) => void;
  dietTypes: (string | Category)[];
  setDietTypes: (diets: string[]) => void;
  restrictions: (string | Category)[];
  setRestrictions: (r: string[]) => void;
  tastes: (string | Category)[];
  setTastes: (t: string[]) => void;
  availableRestrictions?: string[];
  availableTastes?: string[];
};

export type MealItemProps = {
  meal: MealItem;
  onConfirm?: () => void;       // aceptar swap
  onRequestSwap?: () => void;   // solicitar nueva sugerencia
};