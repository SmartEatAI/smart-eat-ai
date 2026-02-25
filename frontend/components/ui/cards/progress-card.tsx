"use client";

import { Card, CardContent } from "@/components/ui/card";
import { useState, useEffect } from "react";

interface ProgressCardProps {
    weeklyData?: {
        day: string;
        percentage: number;
        calories: number;
    }[];
    weeklyAverage?: number;
    weeklyTotal?: number;
}

const ProgressCard: React.FC<ProgressCardProps> = ({ 
    weeklyData = [],
    weeklyAverage = 0,
    weeklyTotal = 0
}) => {
    const [chartPath, setChartPath] = useState<string>("");

    // Generar puntos para el gráfico basados en datos semanales
    useEffect(() => {
        if (weeklyData.length === 0) {
            // Datos de ejemplo si no hay datos reales
            const defaultData = [65, 70, 68, 72, 75, 78, 82];
            generateChartPath(defaultData);
        } else {
            const percentages = weeklyData.map(d => d.percentage);
            generateChartPath(percentages);
        }
    }, [weeklyData]);

    const generateChartPath = (data: number[]) => {
        // Normalizar datos para que quepan en el gráfico (0-100)
        const points = data.map((value, index) => {
            const x = (index / (data.length - 1)) * 300;
            // Invertir Y porque SVG tiene Y=0 arriba (85 es la base, 15 es el tope)
            const y = 85 - (value * 0.7); // Escalar para que quepa entre 15 y 85
            return { x, y };
        });

        // Generar path curvo
        let path = `M ${points[0].x},${points[0].y}`;
        
        for (let i = 1; i < points.length; i++) {
            const prev = points[i - 1];
            const curr = points[i];
            
            // Punto de control para curva suave
            const cp1x = prev.x + (curr.x - prev.x) * 0.3;
            const cp1y = prev.y;
            const cp2x = curr.x - (curr.x - prev.x) * 0.3;
            const cp2y = curr.y;
            
            path += ` C ${cp1x},${cp1y} ${cp2x},${cp2y} ${curr.x},${curr.y}`;
        }
        
        setChartPath(path);
    };

    // Generar puntos de la cuadrícula para los días de la semana
    const dayLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    
    return (
        <Card className="bg-gradient-to-br from-green-950/80 to-green-900/60 border-green-800/50 w-full h-full">
            <CardContent className="p-6 h-full flex flex-col">
                {/* Weekly Stats Summary */}
                <div className="grid grid-cols-2 gap-2 mb-4 text-sm">
                    <div className="bg-green-950/40 p-2 rounded">
                        <span className="text-primary text-xl font-medium">Weekly total</span>
                        <p className="text-muted-foreground">{weeklyTotal} kcal</p>
                    </div>
                    <div className="bg-green-950/40 p-2 rounded">
                        <span className="text-primary text-xl font-medium">Daily avg</span>
                        <p className="text-muted-foreground">{weeklyAverage} kcal</p>
                    </div>
                </div>

                {/* SVG Chart */}
                <div className="relative flex-1 w-full min-h-[8rem]">
                    <svg viewBox="0 0 300 100" className="w-full h-full" preserveAspectRatio="none">
                        {/* Grid lines */}
                        <line x1="0" y1="25" x2="300" y2="25" stroke="rgba(72, 187, 120, 0.1)" strokeWidth="1" />
                        <line x1="0" y1="50" x2="300" y2="50" stroke="rgba(72, 187, 120, 0.1)" strokeWidth="1" />
                        <line x1="0" y1="75" x2="300" y2="75" stroke="rgba(72, 187, 120, 0.1)" strokeWidth="1" />
                        
                        {/* Vertical grid lines for days */}
                        {dayLabels.map((_, i) => (
                            <line 
                                key={i}
                                x1={i * 42.8} 
                                y1="15" 
                                x2={i * 42.8} 
                                y2="85" 
                                stroke="rgba(72, 187, 120, 0.05)" 
                                strokeWidth="1" 
                            />
                        ))}
                        
                        {/* Wavy progress line */}
                        {chartPath && (
                            <>
                                <path
                                    d={chartPath}
                                    fill="none"
                                    stroke="rgb(72, 187, 120)"
                                    strokeWidth="3"
                                    strokeLinecap="round"
                                    style={{
                                        filter: "drop-shadow(0 0 8px rgba(72, 187, 120, 0.6))"
                                    }}
                                />
                                
                                {/* Gradient fill under the line */}
                                <defs>
                                    <linearGradient id="progressGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                                        <stop offset="0%" stopColor="rgb(72, 187, 120)" stopOpacity="0.3" />
                                        <stop offset="100%" stopColor="rgb(72, 187, 120)" stopOpacity="0" />
                                    </linearGradient>
                                </defs>
                                <path
                                    d={`${chartPath} L 300,100 L 0,100 Z`}
                                    fill="url(#progressGradient)"
                                />
                            </>
                        )}
                        
                        {/* Day labels */}
                        {dayLabels.map((day, i) => (
                            <text
                                key={i}
                                x={i * 42.8 + 21}
                                y="95"
                                fontSize="8"
                                fill="rgba(255,255,255,0.5)"
                                textAnchor="middle"
                            >
                                {day}
                            </text>
                        ))}
                    </svg>
                </div>
            </CardContent>
        </Card>
    );
};

export default ProgressCard;