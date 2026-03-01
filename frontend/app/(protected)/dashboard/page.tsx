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
import type { PlanResponse } from "@/types/my-plan";
import { useAuth } from "@/hooks/useAuth";

const DAY_NAMES: Record<number, string> = {
    1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday",
    5: "Friday", 6: "Saturday", 7: "Sunday",
};

function transformPlan(plan: PlanResponse | null) {
    if (!plan?.daily_menus) return [];

    return plan.daily_menus
        .sort((a, b) => a.day_of_week - b.day_of_week)
        .map((menu) => ({
            id: menu.id,
            day_of_week: menu.day_of_week,
            name: DAY_NAMES[menu.day_of_week] ?? `Day ${menu.day_of_week}`,
            meals: [...menu.meal_details].sort((a, b) => a.schedule - b.schedule),
        }));
}

export default function Dashboard() {
    const { profile } = useProfile();
    const { user, token } = useAuth();
    const router = useRouter();

    const [weekData, setWeekData] = useState<any[]>([]);
    const [mealList, setMealList] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [hasPlan, setHasPlan] = useState(false);

    const [macronutrients, setMacronutrients] = useState({
        calories: { current: 0, goal: 0 },
        protein: { current: 0, goal: 0 },
        carbs: { current: 0, goal: 0 },
        fats: { current: 0, goal: 0 },
    });

    // 🔥 Fetch plan
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
                if (!res.ok) throw new Error("Error fetching plan");

                setHasPlan(true);
                return res.json();
            })
            .then((data) => {
                if (!data) return;

                const transformed = transformPlan(data);
                setWeekData(transformed);

                // 🔥 Obtener día actual
                const today = new Date().getDay();
                const adjustedDay = today === 0 ? 7 : today;

                const todayMenu = transformed.find(
                    (day) => day.day_of_week === adjustedDay
                );

                if (todayMenu) {
                    setMealList(todayMenu.meals);
                    calculateMacros(todayMenu.meals);
                }
            })
            .catch(() => setHasPlan(false))
            .finally(() => setLoading(false));
    }, [token]);

    // 🔥 Actualizar objetivos cuando cambia profile
    useEffect(() => {
        if (!profile) return;

        setMacronutrients((prev) => ({
            calories: { current: prev.calories.current, goal: profile.calories_target || 0 },
            protein: { current: prev.protein.current, goal: profile.protein_target || 0 },
            carbs: { current: prev.carbs.current, goal: profile.carbs_target || 0 },
            fats: { current: prev.fats.current, goal: profile.fat_target || 0 },
        }));
    }, [profile]);

    function calculateMacros(meals: any[]) {
        const totals = meals.reduce(
            (acc, meal) => {
                if (meal.status === 1) {
                    acc.calories += meal.recipe?.calories || 0;
                    acc.protein += meal.recipe?.protein || 0;
                    acc.carbs += meal.recipe?.carbs || 0;
                    acc.fats += meal.recipe?.fat || 0;
                }
                return acc;
            },
            { calories: 0, protein: 0, carbs: 0, fats: 0 }
        );

        setMacronutrients((prev) => ({
            calories: { current: totals.calories, goal: prev.calories.goal },
            protein: { current: totals.protein, goal: prev.protein.goal },
            carbs: { current: totals.carbs, goal: prev.carbs.goal },
            fats: { current: totals.fats, goal: prev.fats.goal },
        }));
    }

    // 🔥 Toggle Status con backend
    const toggleStatus = async (mealDetailId: number, currentStatus: number) => {
        const newStatus = currentStatus === 1 ? 0 : 1;

        // Optimistic update
        const updatedMeals = mealList.map((meal) =>
            meal.id === mealDetailId
                ? { ...meal, status: newStatus }
                : meal
        );

        setMealList(updatedMeals);
        calculateMacros(updatedMeals);

        try {
            const response = await fetch(
                `http://localhost:8000/api/meal-detail/${mealDetailId}/status?status=${newStatus}`,
                {
                    method: "PUT",
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            if (!response.ok) throw new Error("Failed to update status");
        } catch (error) {
            console.error(error);

            // rollback
            const rollbackMeals = mealList.map((meal) =>
                meal.id === mealDetailId
                    ? { ...meal, status: currentStatus }
                    : meal
            );

            setMealList(rollbackMeals);
            calculateMacros(rollbackMeals);
        }
    };

    if (loading) {
        return (
            <AppLayout title="📊 Dashboard">
                <div className="py-12 text-center text-muted-foreground">
                    Loading your dashboard...
                </div>
            </AppLayout>
        );
    }

    if (!hasPlan) {
        return (
            <AppLayout title="📊 Dashboard">
                <NoPlanCard />
            </AppLayout>
        );
    }

    return (
        <AppLayout
            title="📊 Dashboard"
            subtitle={
                <span className="text-base text-muted-foreground">
                    Hello, <span className="font-semibold text-primary">{user?.name}</span> 👋
                </span>
            }
            subtitleAlign="right"
        >
            {/* Macronutrients */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                <div className="lg:col-span-2">
                    <MacronutrientCard {...macronutrients} />
                </div>
            </div>

            {/* Today's Meals */}
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
                            className="flex items-center justify-between p-4 bg-card rounded-lg shadow-md"
                        >
                            <div className="flex items-center gap-4 flex-1">
                                <div className="w-16 h-16 relative">
                                    <Image
                                        src={meal.recipe?.image_url?.split(", ").map(img => img.trim())[0] || "/images/Image_not_available.png"}
                                        alt={meal.recipe?.name}
                                        fill
                                        className="object-cover rounded-md"
                                    />
                                </div>
                                <div>
                                    <h3 className="text-lg font-semibold text-primary">
                                        {meal.recipe?.name}
                                    </h3>
                                    <p className="text-xs text-muted-foreground mt-1">
                                        {meal.recipe?.calories} kcal •
                                        {meal.recipe?.protein}g Prot •
                                        {meal.recipe?.carbs}g Carb •
                                        {meal.recipe?.fat}g Fat
                                    </p>
                                </div>
                            </div>

                            <Button
                                variant={meal.status === 1 ? "primary" : "secondary"}
                                onClick={() => toggleStatus(meal.id, meal.status)}
                            >
                                {meal.status === 1 ? (
                                    <>
                                        <Check className="h-4 w-4 mr-1" />
                                        Consumed
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