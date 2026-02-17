"use client";

import { Card, CardContent } from "@/components/ui/card";

const ProgressCard: React.FC = () => {
    return (
        <Card className="bg-gradient-to-br from-green-950/80 to-green-900/60 border-green-800/50 w-full h-full">
            <CardContent className="p-6 h-full flex flex-col">
                <div className="flex items-start justify-between mb-6">
                    <div>
                        <h2 className="text-lg font-semibold text-primary">Weekly</h2>
                        <h3 className="text-lg font-semibold text-primary">Trend</h3>
                    </div>
                    <div className="text-right">
                        <span className="text-primary text-sm font-semibold">+2% vs</span>
                        <div className="text-primary text-sm">average</div>
                    </div>
                </div>

                {/* SVG Chart */}
                <div className="relative flex-1 w-full min-h-[8rem]">
                    <svg viewBox="0 0 300 100" className="w-full h-full" preserveAspectRatio="none">
                        {/* Grid lines */}
                        <line x1="0" y1="25" x2="300" y2="25" stroke="rgba(72, 187, 120, 0.1)" strokeWidth="1" />
                        <line x1="0" y1="50" x2="300" y2="50" stroke="rgba(72, 187, 120, 0.1)" strokeWidth="1" />
                        <line x1="0" y1="75" x2="300" y2="75" stroke="rgba(72, 187, 120, 0.1)" strokeWidth="1" />
                        
                        {/* Wavy progress line */}
                        <path
                            d="M 0,70 Q 30,85 50,75 T 100,60 T 150,45 T 200,35 T 250,25 Q 270,20 300,15"
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
                            d="M 0,70 Q 30,85 50,75 T 100,60 T 150,45 T 200,35 T 250,25 Q 270,20 300,15 L 300,100 L 0,100 Z"
                            fill="url(#progressGradient)"
                        />
                    </svg>
                </div>
            </CardContent>
        </Card>
    );
};

export default ProgressCard;
