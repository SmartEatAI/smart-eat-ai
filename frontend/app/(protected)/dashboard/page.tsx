"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import MacronutrientCard from "@/components/ui/cards/macronutrient-card";
import ProgressCard from "@/components/ui/cards/progress-card";
import { useState, useEffect } from "react";
import { useProfile } from "@/hooks/useProfile";
import Image from "next/image";
import Button from "@/components/ui/Button";
import { Check } from "lucide-react";
import NoPlanCard from "@/components/my-plan/NoPlanCard";
import { useRouter } from "next/navigation";
import type { Meal, DailyMenu, WeeklyStats, WeeklyDayData } from "@/types/dashboard";
import { useAuth } from "@/hooks/useAuth";

const DAY_NAMES: Record<number, string> = {
    1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday",
    5: "Friday", 6: "Saturday", 7: "Sunday",
};

function getAllImages(image_url: string | null | undefined): string[] {
    if (!image_url) return [];
    return image_url
        .split(/,\s*(?=https?:\/\/)/)
        .map((u) => u.trim())
        .filter(Boolean);
}

function transformPlan(plan: any): DailyMenu[] {
    if (!plan?.daily_menus) return [];
    return plan.daily_menus
        .sort((a: any, b: any) => a.day_of_week - b.day_of_week)
        .map((menu: any) => ({
            name: DAY_NAMES[menu.day_of_week] ?? `Day ${menu.day_of_week}`,
            meals: (menu.meal_details ?? []).map((detail: any) => {
                const images = getAllImages(detail.recipe?.image_url);
                return {
                    id: detail.id,
                    recipeId: detail.recipe_id,
                    name: detail.recipe?.name ?? "Unknown recipe",
                    title: detail.recipe?.name ?? "Unknown recipe",
                    calories: detail.recipe?.calories ?? 0,
                    protein: detail.recipe?.protein ?? 0,
                    carbs: detail.recipe?.carbs ?? 0,
                    fat: detail.recipe?.fat ?? 0,
                    description: detail.meal_type ?? "",
                    images: images,
                    image: images[0] || "/images/Image_not_available.png",
                    mealType: detail.meal_type,
                    schedule: detail.schedule,
                    consumed: false,
                };
            }),
        }));
}

// Función para calcular datos semanales
function calculateWeeklyData(weekData: DailyMenu[], dailyGoal: number): WeeklyStats {
    if (!weekData.length) return { weeklyData: [], weeklyAverage: 0, weeklyTotal: 0 };

    //Calcular el total de calorías por cada día
    const weeklyData: WeeklyDayData[] = weekData.map(day => {
        // Sumar las calorías de todas las comidas del día
        const totalCalories = day.meals.reduce((sum, meal) => sum + meal.calories, 0);
        // Calcular el porcentaje respecto al objetivo diario
        const percentage = dailyGoal > 0 ? Math.min(Math.round((totalCalories / dailyGoal) * 100), 100) : 0;
        
        return {
            day: day.name,
            percentage,
            calories: totalCalories
        };
    });

    // Calcular el total semanal entre nº de días y el promedio semanal
    const weeklyTotal = weeklyData.reduce((sum, day) => sum + day.calories, 0);
    const weeklyAverage = weekData.length > 0 ? Math.round(weeklyTotal / weekData.length) : 0;

    return { weeklyData, weeklyAverage, weeklyTotal };
}

export default function Dashboard() {
    const { profile } = useProfile();
    const { user, token } = useAuth();
    const router = useRouter();
    const [weekData, setWeekData] = useState<DailyMenu[]>([]);
    const [todaysMeals, setTodaysMeals] = useState<Meal[]>([]);
    const [loading, setLoading] = useState(true);
    const [hasPlan, setHasPlan] = useState(false);
    const [macronutrients, setMacronutrients] = useState({
        calories: { current: 0, goal: 0 },
        protein: { current: 0, goal: 0 },
        carbs: { current: 0, goal: 0 },
        fats: { current: 0, goal: 0 },
    });
    const [mealList, setMealList] = useState<Meal[]>([]);
    const [weeklyStats, setWeeklyStats] = useState<WeeklyStats>({
        weeklyData: [],
        weeklyAverage: 0,
        weeklyTotal: 0
    });


    // Fetch plan data
    useEffect(() => {
        if (!token) {
            router.push("/login");
            return;
        }

        fetch("http://localhost:8000/api/plan/current", {
            headers: { Authorization: `Bearer ${token}` },
        })
            .then((res) => {
                if (res.status === 404) {
                    setHasPlan(false);
                    setLoading(false);
                    return null;
                }
                if (!res.ok) {
                    throw new Error("Error fetching plan");
                }
                setHasPlan(true);
                return res.json();
            })
            .then((data) => {
                if (data) {
                    const transformedData = transformPlan(data);
                    setWeekData(transformedData);
                    
                    // Calcular estadísticas semanales
                    const dailyGoal = profile?.calories_target || 2000;
                    const stats = calculateWeeklyData(transformedData, dailyGoal);
                    setWeeklyStats(stats);
                    
                    // Recuperar el menú del día actual
                    const today = new Date().getDay(); // 0 = Sunday, 1 = Monday, etc.
                    const adjustedDay = today === 0 ? 7 : today;
                    
                    const todayMenu = transformedData.find(day => {
                        const dayNumber = Object.keys(DAY_NAMES).find(
                            key => DAY_NAMES[parseInt(key)] === day.name
                        );
                        return parseInt(dayNumber || '0') === adjustedDay;
                    });

                    if (todayMenu) {
                        setTodaysMeals(todayMenu.meals);
                        setMealList(todayMenu.meals);
                        
                        // Calculate current macros for today
                        const totals = todayMenu.meals.reduce(
                            (acc, meal) => ({
                                calories: acc.calories + (meal.consumed ? meal.calories : 0),
                                protein: acc.protein + (meal.consumed ? meal.protein : 0),
                                carbs: acc.carbs + (meal.consumed ? meal.carbs : 0),
                                fats: acc.fats + (meal.consumed ? meal.fat : 0),
                            }),
                            { calories: 0, protein: 0, carbs: 0, fats: 0 }
                        );

                        setMacronutrients(prev => ({
                            calories: { current: totals.calories, goal: prev.calories.goal },
                            protein: { current: totals.protein, goal: prev.protein.goal },
                            carbs: { current: totals.carbs, goal: prev.carbs.goal },
                            fats: { current: totals.fats, goal: prev.fats.goal },
                        }));
                    }
                }
            })
            .catch((error) => {
                console.error("Error fetching plan:", error);
                setHasPlan(false);
            })
            .finally(() => setLoading(false));
    }, [router, profile]);

    // Update macros goals when profile changes
    useEffect(() => {
        if (profile) {
            setMacronutrients(prev => ({
                calories: { current: prev.calories.current, goal: profile.calories_target || 0 },
                protein: { current: prev.protein.current, goal: profile.protein_target || 0 },
                carbs: { current: prev.carbs.current, goal: profile.carbs_target || 0 },
                fats: { current: prev.fats.current, goal: profile.fat_target || 0 },
            }));
        }
    }, [profile]);

    // Helper to render mealType as badge(s)
    const renderMealTypeBadge = (mealType: any) => {
        if (!mealType) return null;
        let types: string[] = [];
        if (Array.isArray(mealType)) {
            types = mealType.map((mt) => typeof mt === 'string' ? mt : (mt?.name ?? String(mt)));
        } else if (typeof mealType === 'string' && mealType) {
            types = [mealType];
        } else if (mealType?.name) {
            types = [mealType.name];
        }
        return (
            <div className="flex flex-wrap gap-1 mb-2 mt-1">
                {types.map((badge, idx) => (
                    <span
                        key={idx}
                        className="inline-block bg-primary/10 text-primary text-xs font-semibold px-2 py-0.5 rounded-full border border-primary/20 tracking-wide"
                    >
                        {badge.charAt(0).toUpperCase() + badge.slice(1)}
                    </span>
                ))}
            </div>
        );
    };

    const toggleConsumed = (id: number) => {
        setMealList((prevMeals) => {
            const updatedMeals = prevMeals.map((meal) =>
                meal.id === id ? { ...meal, consumed: !meal.consumed } : meal
            );

            // Recalculate macros based on consumed meals
            const totals = updatedMeals.reduce(
                (acc, meal) => ({
                    calories: acc.calories + (meal.consumed ? meal.calories : 0),
                    protein: acc.protein + (meal.consumed ? meal.protein : 0),
                    carbs: acc.carbs + (meal.consumed ? meal.carbs : 0),
                    fats: acc.fats + (meal.consumed ? meal.fat : 0),
                }),
                { calories: 0, protein: 0, carbs: 0, fats: 0 }
            );

            setMacronutrients(prev => ({
                calories: { current: totals.calories, goal: prev.calories.goal },
                protein: { current: totals.protein, goal: prev.protein.goal },
                carbs: { current: totals.carbs, goal: prev.carbs.goal },
                fats: { current: totals.fats, goal: prev.fats.goal },
            }));

            return updatedMeals;
        });
    };

    if (loading) {
        return (
            <AppLayout
                title="📊 Dashboard"
                subtitle={
                    <span className="text-base md:text-lg text-muted-foreground">
                        Hello, <span className="font-semibold text-primary">{user?.name || "Guest"}</span> 👋
                    </span>
                }
                subtitleAlign="right"
            >
                <div className="py-12 text-center text-muted-foreground">
                    Loading your dashboard...
                </div>
            </AppLayout>
        );
    }

    if (!hasPlan) {
        return (
            <AppLayout
                title="📊 Dashboard"
                subtitle={
                    <span className="text-base md:text-lg text-muted-foreground">
                        Hello, <span className="font-semibold text-primary">{user?.name || "Guest"}</span> 👋
                    </span>
                }
                subtitleAlign="right"
            >
                {/* Cards Grid always visible */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                    <div className="lg:col-span-2">
                        <MacronutrientCard 
                            calories={macronutrients.calories}
                            protein={macronutrients.protein}
                            carbs={macronutrients.carbs}
                            fats={macronutrients.fats}
                        />
                    </div>
                    <div className="lg:col-span-1">
                        <ProgressCard 
                            weeklyData={weeklyStats.weeklyData}
                            weeklyAverage={weeklyStats.weeklyAverage}
                            weeklyTotal={weeklyStats.weeklyTotal}
                        />
                    </div>
                </div>
                <NoPlanCard />
            </AppLayout>
        );
    }

    return (
        <AppLayout
            title="📊 Dashboard"
            subtitle={
                <span className="text-base md:text-lg text-muted-foreground">
                    Hello, <span className="font-semibold text-primary">{user?.name || "Guest"}</span> 👋
                </span>
            }
            subtitleAlign="right"
        >
            {/* Cards Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                {/* Macronutrients Card */}
                <div className="lg:col-span-2">
                    <MacronutrientCard 
                        calories={macronutrients.calories}
                        protein={macronutrients.protein}
                        carbs={macronutrients.carbs}
                        fats={macronutrients.fats}
                    />
                </div>

                {/* Progress Card */}
                <div className="lg:col-span-1">
                    <ProgressCard 
                        weeklyData={weeklyStats.weeklyData}
                        weeklyAverage={weeklyStats.weeklyAverage}
                        weeklyTotal={weeklyStats.weeklyTotal}
                    />
                </div>
            </div>

            {/* Today's Meal Schedule Section */}
            <h2 className="text-2xl font-bold tracking-tight text-primary mb-4 border-b border-muted pb-2">
                Today&apos;s Meals
            </h2>

            {mealList.length === 0 ? (
                <div className="py-12 text-center text-muted-foreground">
                    No meals scheduled for today.
                </div>
            ) : (
                <div className="space-y-4">
                    {mealList.map((meal) => (
                        <div
                            key={meal.id}
                            className="flex items-center justify-between p-4 bg-card rounded-lg shadow-md hover:shadow-lg transition-shadow"
                        >
                            <div className="flex items-center gap-4 flex-1">
                                <div className="w-16 h-16 relative flex-shrink-0">
                                    <Image
                                        src={meal.image}
                                        alt={meal.name}
                                        fill
                                        className="object-cover rounded-md"
                                        onError={(e) => {
                                            // Fallback image if the recipe image fails to load
                                            const target = e.target as HTMLImageElement;
                                            target.src = "/images/Image_not_available.png";
                                        }}
                                    />
                                </div>
                                <div className="flex-1">
                                    <h3 className="text-lg font-semibold text-primary">
                                        {meal.name}
                                    </h3>
                                    {renderMealTypeBadge(meal.mealType)}
                                    <p className="text-xs text-muted-foreground mt-1">
                                        {meal.calories} kcal • {meal.protein}g Prot • {meal.carbs}g Carb • {meal.fat}g Fat
                                    </p>
                                </div>
                            </div>
                            <Button
                                variant={meal.consumed ? "primary" : "secondary"}
                                className="shadow-md flex items-center gap-2 ml-4 flex-shrink-0"
                                onClick={() => toggleConsumed(meal.id)}
                            >
                                {meal.consumed ? (
                                    <>
                                        <Check className="h-4 w-4" /> Consumed
                                    </>
                                ) : (
                                    "Mark as consumed"
                                )}
                            </Button>
                        </div>
                    ))}
                </div>
            )}
        </AppLayout>
    );
}