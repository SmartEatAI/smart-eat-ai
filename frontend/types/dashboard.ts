export interface Meal {
    id: number;
    name: string;
    time: string;
    image: string;
    calories: number;
    protein: number;
    carbs: number;
    fat: number;
    consumed: boolean;
    recipeId?: number;
    mealType?: string;
    schedule?: string;
}

export interface DailyMenu {
    name: string;
    meals: Meal[];
}

export interface WeeklyDayData {
    day: string;
    percentage: number;
    calories: number;
}

export interface WeeklyStats {
    weeklyData: WeeklyDayData[];
    weeklyAverage: number;
    weeklyTotal: number;
}