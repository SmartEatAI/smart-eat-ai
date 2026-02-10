"use client";

import React from "react";
import { Card, CardContent } from "@/components/ui/card";

interface MacronutrientCardProps {
    calories: { current: number; goal: number };
    protein: { current: number; goal: number };
    carbs: { current: number; goal: number };
    fats: { current: number; goal: number };
}

const MacronutrientCard: React.FC<MacronutrientCardProps> = ({
    calories,
    protein,
    carbs,
    fats,
}) => {
    const caloriesRemaining = calories.goal - calories.current;
    const caloriesPercentage = Math.min((calories.current / calories.goal) * 100, 100);
    const proteinPercentage = (protein.current / protein.goal) * 100;
    const carbsPercentage = (carbs.current / carbs.goal) * 100;
    const fatsPercentage = (fats.current / fats.goal) * 100;

    return (
        <Card className="bg-gradient-to-br from-green-950/80 to-green-900/60 border-green-800/50 w-full h-full">
            <CardContent className="p-6 h-full flex flex-col">
                <div className="flex flex-col items-center mb-6">
                    <h2 className="text-xl font-semibold text-primary flex items-center gap-2">
                        Calorías y Macros
                    </h2>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                    {/* Círculo de progreso de calorías */}
                    <div className="flex items-center justify-center">
                        <div className="relative w-48 h-48">
                            <svg className="w-full h-full transform -rotate-90">
                                {/* Círculo de fondo */}
                                <circle
                                    cx="96"
                                    cy="96"
                                    r="88"
                                    className="fill-none stroke-green-900/30"
                                    strokeWidth="12"
                                />
                                {/* Círculo de progreso */}
                                <circle
                                    cx="96"
                                    cy="96"
                                    r="88"
                                    className="fill-none stroke-primary"
                                    strokeWidth="12"
                                    strokeLinecap="round"
                                    strokeDasharray={`${2 * Math.PI * 88}`}
                                    strokeDashoffset={`${2 * Math.PI * 88 * (1 - caloriesPercentage / 100)}`}
                                    style={{
                                        transition: "stroke-dashoffset 0.5s ease-in-out",
                                        filter: "drop-shadow(0 2px 2px rgba(72, 187, 120, 0.6))", // Efecto de halo
                                    }}
                                />
                            </svg>
                            <div className="absolute inset-0 flex flex-col items-center justify-center">
                                <p className="text-xs text-muted-foreground uppercase tracking-wider">Restantes</p>
                                <p className="text-4xl font-bold text-primary">{caloriesRemaining}</p>
                                <p className="text-xs text-muted-foreground">de {calories.goal} kcal</p>
                            </div>
                        </div>
                    </div>

                    {/* Barras de progreso de macros */}
                    <div className="space-y-6">
                        {/* Proteína */}
                        <div>
                            <div className="flex items-center justify-between mb-2">
                                <div className="flex items-center gap-2">
                                    <div className="w-3 h-3 rounded-full bg-chart-1"></div>
                                    <span className="text-sm font-medium text-primary">Proteína</span>
                                </div>
                                <span className="text-sm text-muted-foreground">
                                    {protein.current}g / {protein.goal}g
                                </span>
                            </div>
                            <div className="w-full h-2 bg-green-900/30 rounded-full overflow-hidden">
                                <div
                                    className="h-full bg-chart-1 rounded-full transition-all duration-500"
                                    style={{ width: `${Math.min(proteinPercentage, 100)}%` }}
                                ></div>
                            </div>
                        </div>

                        {/* Carbohidratos */}
                        <div>
                            <div className="flex items-center justify-between mb-2">
                                <div className="flex items-center gap-2">
                                    <div className="w-3 h-3 rounded-full bg-chart-2"></div>
                                    <span className="text-sm font-medium text-primary">Carbohidratos</span>
                                </div>
                                <span className="text-sm text-muted-foreground">
                                    {carbs.current}g / {carbs.goal}g
                                </span>
                            </div>
                            <div className="w-full h-2 bg-green-900/30 rounded-full overflow-hidden">
                                <div
                                    className="h-full bg-chart-2 rounded-full transition-all duration-500"
                                    style={{ width: `${Math.min(carbsPercentage, 100)}%` }}
                                ></div>
                            </div>
                        </div>

                        {/* Grasas */}
                        <div>
                            <div className="flex items-center justify-between mb-2">
                                <div className="flex items-center gap-2">
                                    <div className="w-3 h-3 rounded-full bg-chart-3"></div>
                                    <span className="text-sm font-medium text-primary">Grasas</span>
                                </div>
                                <span className="text-sm text-muted-foreground">
                                    {fats.current}g / {fats.goal}g
                                </span>
                            </div>
                            <div className="w-full h-2 bg-green-900/30 rounded-full overflow-hidden">
                                <div
                                    className="h-full bg-chart-3 rounded-full transition-all duration-500"
                                    style={{ width: `${Math.min(fatsPercentage, 100)}%` }}
                                ></div>
                            </div>
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
};

export default MacronutrientCard;