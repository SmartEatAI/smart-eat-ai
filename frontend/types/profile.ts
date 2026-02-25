import {Category} from "@/types/category"

export interface Profile {
  id: number;
  user_id: number;
  goal: string;
  height: number;
  weight: number;
  body_type: string;
  gender: string;
  meals_per_day: number;
  activity_level: string;
  birth_date: string;
  body_fat_percentage?: number;
  calories_target?: number;
  protein_target?: number;
  carbs_target?: number;
  fat_target?: number;
  tastes?: Category[];
  restrictions?: Category[];
  diet_types?: Category[];
}
