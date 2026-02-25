"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import ProtectedRoute from "@/components/auth/ProtectedRoute";
import { 
    Carousel, 
    CarouselContent, 
    CarouselItem, 
    CarouselNext, 
    CarouselPrevious 
} from "@/components/ui/carousel";
import RecipeCard from "@/components/ui/cards/recipe-card";
import MacronutrientCard from "@/components/ui/cards/macronutrient-card";
import ProgressCard from "@/components/ui/cards/progress-card";
import { useState, useEffect } from "react";
import { useProfile } from "@/hooks/useProfile";
import Image from "next/image";
import Button from "@/components/ui/Button";
import { Check } from "lucide-react";
import type { User } from "@/types/user";


const mockRecipes = [
    {
        title: "Omelette with Ham",
        calories: 350,
        image: "/images/receta_1.jpg",
    },
    {
        title: "Gnocci with Tuna",
        calories: 550,
        image: "/images/receta_2.jpg",
    },
    {
        title: "Salmon with Salad",
        calories: 480,
        image: "/images/receta_3.jpg",
    },
    {
        title: "Seafood Creamy Soup",
        calories: 420,
        image: "/images/receta_4.jpg",
    },
    {
        title: "Sweet Potato Fries",
        calories: 390,
        image: "/images/receta_5.jpg",
    },
];

interface Meal {
    id: number;
    name: string;
    time: string;
    image: string;
    calories: number;
    protein: number;
    carbs: number;
    fat: number;
    consumed: boolean;
}

const meals: Meal[] = [
    {
        id: 1,
        name: "Omelette with Ham",
        time: "08:00 AM",
        image: "/images/receta_1.jpg",
        calories: 350,
        protein: 20,
        carbs: 5,
        fat: 25,
        consumed: false,
    },
    {
        id: 2,
        name: "Gnocci with Tuna",
        time: "01:30 PM",
        image: "/images/receta_2.jpg",
        calories: 550,
        protein: 30,
        carbs: 60,
        fat: 15,
        consumed: false,
    },
    {
        id: 3,
        name: "Salmon with Salad",
        time: "07:00 PM",
        image: "/images/receta_3.jpg",
        calories: 480,
        protein: 40,
        carbs: 10,
        fat: 30,
        consumed: false,
    },
    {
        id: 4,
        name: "Seafood Creamy Soup",
        time: "12:00 PM",
        image: "/images/receta_4.jpg",
        calories: 420,
        protein: 25,
        carbs: 20,
        fat: 15,
        consumed: false,
    },
    {
        id: 5,
        name: "Sweet Potato Fries",
        time: "04:00 PM",
        image: "/images/receta_5.jpg",
        calories: 390,
        protein: 5,
        carbs: 50,
        fat: 20,
        consumed: false,
    },
];


export default function Dashboard() {
    const { profile } = useProfile();
    const [macronutrients, setMacronutrients] = useState({
        calories: { current: 0, goal: 0 },
        protein: { current: 0, goal: 0 },
        carbs: { current: 0, goal: 0 },
        fats: { current: 0, goal: 0 },
    });
    const [recipes] = useState(mockRecipes);
    const [user, setUser] = useState<User | null>(null);
    const [mealList, setMealList] = useState(meals);

    // Load user data from localStorage
    useEffect(() => {
        const userData = localStorage.getItem("user");
        if (userData) {
            try {
                const parsedUser = JSON.parse(userData);
                setUser(parsedUser);
            } catch (error) {
                console.error("Error parsing user data:", error);
                setUser(null);
            }
        }
    }, []);

    // Actualizar macros goal cuando cambia el profile
    useEffect(() => {
        if (profile) {
            setMacronutrients({
                calories: { current: 0, goal: profile.calories_target || 0 },
                protein: { current: 0, goal: profile.protein_target || 0 },
                carbs: { current: 0, goal: profile.carbs_target || 0 },
                fats: { current: 0, goal: profile.fat_target || 0 },
            });
        }
    }, [profile]);

    const updateMacro = (
        macroType: 'calories' | 'protein' | 'carbs' | 'fats',
        newValue: { current?: number; goal?: number }
    ) => {
        setMacronutrients((prev) => ({
            ...prev,
            [macroType]: { ...prev[macroType], ...newValue },
        }));
    };

    const toggleConsumed = (id: number) => {
        setMealList((prevMeals) =>
            prevMeals.map((meal) =>
                meal.id === id ? { ...meal, consumed: !meal.consumed } : meal
            )
        );
    };

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
                        <ProgressCard />
                    </div>
                </div>

                {/* Meal Schedule Section */}
                <h2 className="text-2xl font-bold tracking-tight text-primary mb-4 border-b border-muted pb-2">Meal Schedule</h2>
                <div className="space-y-4">
                    {mealList.map((meal) => (
                        <div
                            key={meal.id}
                            className="flex items-center justify-between p-4 bg-card rounded-lg shadow-md"
                        >
                            <div className="flex items-center gap-4">
                                <div className="w-16 h-16 relative">
                                    <Image
                                        src={meal.image}
                                        alt={meal.name}
                                        fill
                                        className="object-cover rounded-md"
                                    />
                                </div>
                                <div>
                                    <h3 className="text-lg font-semibold text-primary">
                                        {meal.name}
                                    </h3>
                                    <p className="text-sm text-muted-foreground">
                                        {meal.time} - {meal.calories} kcal - {meal.protein}g Prot - {meal.carbs}g Carb - {meal.fat}g Fat
                                    </p>
                                </div>
                            </div>
                            <Button
                                variant={meal.consumed ? "primary" : "secondary"}
                                className="shadow-md flex items-center gap-2"
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

                {/* Recommended Recipes Carousel */}
                <h2 className="text-2xl font-bold tracking-tight text-primary my-4 border-b border-muted pb-2">Recommended Recipes</h2>
                <div className="relative">
                    <Carousel opts={{ loop: true, align: "start" }} className="w-full">
                        <CarouselContent className="-ml-2 md:-ml-4">
                            {recipes.map((recipe, index) => (
                                <CarouselItem key={index} className="pl-2 md:pl-4 md:basis-1/2 lg:basis-1/3">
                                    <RecipeCard {...recipe} />
                                </CarouselItem>
                            ))}
                        </CarouselContent>
                        <CarouselPrevious className="hidden lg:flex left-2" />
                        <CarouselNext className="hidden lg:flex right-2" />
                    </Carousel>
                </div>
            </AppLayout>
    );
}