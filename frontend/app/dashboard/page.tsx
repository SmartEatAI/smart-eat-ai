"use client";

import Sidebar from "@/components/layout/Sidebar";
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

const mockMacronutrients = {
    calories: { current: 800, goal: 2100 },
    protein: { current: 120, goal: 150 },
    carbs: { current: 100, goal: 200 },
    fats: { current: 45, goal: 60 },
};

const mockUser = {
    name: "testUser",
    email: "testUser@example.com",
};

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

export default function Dashboard() {
    const [macronutrients, setMacronutrients] = useState(mockMacronutrients);
    const [recipes] = useState(mockRecipes);
    const [user, setUser] = useState(mockUser);

    // ========== DESARROLLO: Sincronizar con mockMacronutrients ==========
    // Comentar o eliminar este useEffect cuando se conecte con el backend real
    useEffect(() => {
        setMacronutrients(mockMacronutrients);
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [mockMacronutrients]);

    // ========== PRODUCCIÓN: Fetch de datos reales del backend ==========
    // Descomentar este useEffect cuando conecte con la API
    // useEffect(() => {
    //     const fetchMacronutrients = async () => {
    //         try {
    //             const response = await fetch('/api/user/macronutrients', {
    //                 headers: {
    //                     'Authorization': `Bearer ${/* tu token de autenticación */}`,
    //                 },
    //             });
    //             if (!response.ok) throw new Error('Error al obtener macronutrientes');
    //             const data = await response.json();
    //             setMacronutrients(data);
    //         } catch (error) {
    //             console.error('Error fetching macronutrients:', error);
    //             // Opcionalmente: mostrar mensaje de error al usuario
    //         }
    //     };
    //     fetchMacronutrients();
    // }, []); // Solo se ejecuta al montar el componente

    // ========== PRODUCCIÓN: Fetch de datos del usuario ==========
    // Descomentar este useEffect cuando conectes con tu API
    // useEffect(() => {
    //     const fetchUserData = async () => {
    //         try {
    //             const response = await fetch('/api/user/profile', {
    //                 headers: {
    //                     'Authorization': `Bearer ${/* tu token de autenticación */}`,
    //                 },
    //             });
    //             if (!response.ok) throw new Error('Error al obtener datos del usuario');
    //             const data = await response.json();
    //             setUser(data);
    //         } catch (error) {
    //             console.error('Error fetching user data:', error);
    //         }
    //     };
    //     fetchUserData();
    // }, []);

    // Función para actualizar cualquier macronutriente dinámicamente
    const updateMacro = (
        macroType: 'calories' | 'protein' | 'carbs' | 'fats',
        newValue: { current?: number; goal?: number }
    ) => {
        setMacronutrients((prev) => ({
            ...prev,
            [macroType]: { ...prev[macroType], ...newValue },
        }));
    };

    return (
        <div className="flex min-h-screen">
            <Sidebar />
            <main className="flex-1 p-6 pt-20 md:pt-6 bg-background text-secondary">
                <div className="flex items-center justify-between mb-6">
                    <h1 className="text-2xl font-bold text-primary">📊 Dashboard</h1>
                    <p className="text-lg text-muted-foreground">
                        Hola, <span className="font-semibold text-primary">{user.name}</span> 👋
                    </p>
                </div>

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

                {/* Recommended Recipes Carousel */}
                <h2 className="text-xl font-semibold mb-4 text-primary">Recommended Recipes</h2>
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
            </main>
        </div>
    );
}