"use client";

import { useRef, useEffect, useState, Fragment } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import MessageBubble from "@/components/chat/MessageBubble";
import ProposalCard from "@/components/chat/ProposalCard";
import TypingIndicator from "@/components/chat/TypingIndicator";
import ChatInput from "@/components/chat/ChatInput";
import { useAuth } from "@/hooks/useAuth";
import { Message, MessageBase, MessageSuggestion, Recipe } from "@/types/chat";

// Dummy inicial
const defaultMessages: Message[] = [
    {
        role: "chef",
        time: new Date(),
        text: "Hello! I've analyzed your current plan. How are you feeling today or what would you like to adjust in your diet?",
    },
    {
        role: "user",
        time: new Date(),
        text: "I want fewer carbs at night.",
    },
    {
        role: "chef",
        time: new Date(),
        text: "Understood. I'll recommend a dinner with fewer carbohydrates.",
    },
    {
        role: "chef",
        time: new Date(),
        text: "Dinner Substitution",
        sustitution: {
            original: {
                recipe_id: 38,
                name: "Lowfat Berry Blue Frozen Dessert",
                image_url:
                    "https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/38/YUeirxMLQaeE1h3v3qnM_229%20berry%20blue%20frzn%20dess.jpg",
                calories: 42.72,
                protein: 0.8,
                carbs: 9.28,
                fat: 0.62,
                meal_types: ["snack"],
                diet_types: ["high_fiber", "low_calorie", "low_carb", "vegetarian"],
                recipe_url: "https://www.food.com/recipe/recipe-38",
            },
            alternative: {
                recipe_id: 101,
                name: "Chicken Salad",
                image_url:
                    "https://images.unsplash.com/photo-1617196031683-5e7b3a1d2c26?crop=entropy&cs=tinysrgb&fit=max&h=416&w=555",
                calories: 450,
                protein: 35,
                carbs: 20,
                fat: 15,
                meal_types: ["dinner"],
                diet_types: ["low_carb", "high_protein"],
                recipe_url: "https://www.food.com/recipe/chicken-salad-101",
            },
            accepted: false,
        },
    },
];

export default function ChatPage() {
    const { user, token } = useAuth();
    const [messages, setMessages] = useState<Message[]>(defaultMessages);
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Scroll automático
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    // Enviar mensaje
    async function handleSendMessage(text: string) {
        const userMessage: MessageBase = {
            role: "user",
            text,
            time: new Date(),
        };
        setMessages((prev) => [...prev, userMessage]);
        setIsLoading(true);

        // Simulación de respuesta con sugerencia dummy
        setTimeout(() => {
            const chefMessage: MessageSuggestion = {
                role: "chef",
                text: "Dinner Substitution",
                time: new Date(),
                sustitution: {
                    original: {
                        recipe_id: 45,
                        name: "Spaghetti Carbonara",
                        image_url:
                            "https://images.unsplash.com/photo-1604908177522-4d3a230cf3d3?crop=entropy&cs=tinysrgb&fit=max&h=416&w=555",
                        calories: 800,
                        protein: 25,
                        carbs: 85,
                        fat: 35,
                        meal_types: ["dinner"],
                        diet_types: ["high_carb", "moderate_fat"],
                        recipe_url: "https://www.food.com/recipe/spaghetti-carbonara-45",
                    },
                    alternative: {
                        recipe_id: 102,
                        name: "Grilled Salmon Salad",
                        image_url:
                            "https://images.unsplash.com/photo-1600891964599-f61ba0e24092?crop=entropy&cs=tinysrgb&fit=max&h=416&w=555",
                        calories: 420,
                        protein: 40,
                        carbs: 15,
                        fat: 20,
                        meal_types: ["dinner"],
                        diet_types: ["low_carb", "high_protein"],
                        recipe_url: "https://www.food.com/recipe/grilled-salmon-salad-102",
                    },
                    accepted: false,
                },
            };
            setMessages((prev) => [...prev, chefMessage]);
            setIsLoading(false);
        }, 1500);
    }

    // Integracion recibir otra receta
    async function fetchNewRecipe(mealType: string, recipeId: number) {
        try {
            const response = await fetch(`http://localhost:8000/api/ml/swap-recipe?recipe_id=${recipeId}&meal_label=${mealType}`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            const data = await response.json();
            return data; // Debería contener la nueva receta sugerida
        } catch (error) {
            console.error("Error fetching new recipe:", error);
        }
    }

    // Función para generar un mensaje de sugerencia basado en una receta swap
    async function handleSwapRecipe(originalRecipe: Recipe) {
        setIsLoading(true);
        try {
            const data = await fetchNewRecipe(originalRecipe.meal_types[0], originalRecipe.recipe_id);
            if (!data) return;

            // Construimos el mensaje de chef con la nueva sugerencia
            const chefMessage: MessageSuggestion = {
                role: "chef",
                text: "Swap Recipe Suggestion",
                time: new Date(),
                sustitution: {
                    original: originalRecipe,
                    alternative: {
                        recipe_id: data.recipe_id,
                        name: data.name,
                        image_url: data.image_url,
                        calories: data.calories,
                        protein: data.protein,
                        carbs: data.carbs,
                        fat: data.fat,
                        meal_types: data.meal_types,
                        diet_types: data.diet_types,
                        recipe_url: data.recipe_url,
                    },
                    accepted: false,
                },
            };

            setMessages((prev) => [...prev, chefMessage]);
        } catch (error) {
            console.error("Error swapping recipe:", error);
        } finally {
            setIsLoading(false);
        }
    }
    return (
        <AppLayout title="🤖 Intelligent Nutrition Assistant">
            <div className="flex flex-col h-[80vh]">
                <div className="flex-1 flex flex-col gap-4 p-4 overflow-y-auto scrollbar-hide">
                    {messages.map((msg, i) => (
                        <Fragment key={i}>
                            <MessageBubble
                                role={msg.role}
                                time={msg.time.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                                text={msg.text}
                                avatar="" />

                            {"sustitution" in msg && msg.sustitution && (
                                <ProposalCard
                                    image={msg.sustitution.alternative.image_url?.split(', ').map(img => img.trim())?.[0] ?? ""}
                                    badge="Suggestion"
                                    title={msg.text}
                                    description={`${msg.sustitution.original.name} (${msg.sustitution.original.calories} kcal) → ${msg.sustitution.alternative.name} (${msg.sustitution.alternative.calories} kcal)`}
                                    onConfirm={() =>
                                        setMessages((prev) =>
                                            prev.map((m, idx) =>
                                                idx === i && "sustitution" in m
                                                    ? { ...m, sustitution: { ...m.sustitution, accepted: true } }
                                                    : m
                                            )
                                        )
                                    }
                                    onCancel={() => {
                                        // Al rechazar, podemos hacer swap automático y mostrar nueva receta
                                        handleSwapRecipe(msg.sustitution.original);
                                    }}
                                />
                            )}
                        </Fragment>
                    ))}
                    {isLoading && <TypingIndicator />}
                    <div ref={messagesEndRef} />
                </div>

                <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
            </div>
        </AppLayout>
    );
}