// ===== ENUMS =====
export type MealTypeEnum = "breakfast" | "lunch" | "dinner" | "snack";

// ===== CATEGORY =====
export interface CategoryResponse {
  id: number;
  name: string;
}

// ===== RECIPE =====
export interface RecipeResponse {
  id: number;
  recipe_id: number;
  name: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  image_url?: string | null;
  recipe_url?: string | null;
  meal_types: CategoryResponse[];
  diet_types: CategoryResponse[];
}

// ===== MEAL DETAIL =====
export interface MealDetailResponse {
  id: number;
  recipe_id: number;
  schedule: number;
  status: number;
  meal_type: MealTypeEnum;
  recipe: RecipeResponse;
}

// ===== DAILY MENU =====
export interface DailyMenuResponse {
  id: number;
  day_of_week: number; // 1-7
  meal_details: MealDetailResponse[];
}

// ===== PLAN =====
export interface PlanResponse {
  id: number;
  user_id: number;
  created_at: string; // ISO datetime
  updated_at: string; // ISO datetime
  daily_menus: DailyMenuResponse[];
  active: boolean;
}

export interface UIDayPlan {
  id: number;
  day_of_week: number;
  name: string;
  meals: MealDetailResponse[];
}