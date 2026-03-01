"use client";

import { useRef, useEffect, useState, Fragment } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import MessageBubble from "@/components/chat/MessageBubble";
import ProposalCard from "@/components/chat/ProposalCard";
import TypingIndicator from "@/components/chat/TypingIndicator";
import ChatInput from "@/components/chat/ChatInput";
import { useAuth } from "@/hooks/useAuth";
import { Message, MessageBase, MessageSuggestion, Recipe } from "@/types/chat";

const STORAGE_KEY = "chat_messages";
const EXPIRATION_TIME = 24 * 60 * 60 * 1000; // 24h

export default function ChatPage() {
    const { token } = useAuth();
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // ===============================
    // ESTADO CON CARGA DESDE LOCALSTORAGE + EXPIRACIÓN 24H
    // ===============================
    const [messages, setMessages] = useState<Message[]>(() => {
        if (typeof window === "undefined") return [];

        const stored = localStorage.getItem(STORAGE_KEY);
        if (!stored) return [];

        try {
            const parsed = JSON.parse(stored);

            if (!parsed.length) return [];

            const now = Date.now();
            const lastMessageTime = new Date(
                parsed[parsed.length - 1].time
            ).getTime();

            // 🔥 Si pasaron más de 24h, limpiar
            if (now - lastMessageTime > EXPIRATION_TIME) {
                localStorage.removeItem(STORAGE_KEY);
                return [];
            }

            // Reconstruir Date
            return parsed.map((msg: any) => ({
                ...msg,
                time: new Date(msg.time),
            }));
        } catch {
            return [];
        }
    });

    const [isLoading, setIsLoading] = useState(false);

    // ===============================
    // GUARDADO AUTOMÁTICO EN LOCALSTORAGE
    // ===============================
    useEffect(() => {
        if (typeof window === "undefined") return;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
    }, [messages]);

    // ===============================
    // SCROLL AUTOMÁTICO
    // ===============================
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    // ===============================
    // ENVIAR MENSAJE AL BACKEND
    // ===============================
    async function handleSendMessage(text: string) {
        if (!token || !text.trim()) return;

        const userMessage: MessageBase = {
            role: "user",
            text,
            time: new Date(),
        };

        setMessages((prev) => [...prev, userMessage]);
        setIsLoading(true);

        try {
            const response = await fetch(
                `http://localhost:8000/api/chat/?message=${encodeURIComponent(
                    text
                )}`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            if (!response.ok) {
                throw new Error("Chat request failed");
            }

            const data = await response.json();

            const chefMessage: MessageBase = {
                role: "chef",
                text: data.response,
                time: new Date(),
            };

            setMessages((prev) => [...prev, chefMessage]);
        } catch (error) {
            console.error("Chat error:", error);
        } finally {
            setIsLoading(false);
        }
    }

    // ===============================
    // SWAP RECIPE
    // ===============================
    async function fetchNewRecipe(mealType: string, recipeId: number) {
        try {
            const response = await fetch(
                `http://localhost:8000/api/ml/swap-recipe?recipe_id=${recipeId}&meal_label=${mealType}`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            if (!response.ok) {
                throw new Error("Swap recipe failed");
            }

            return await response.json();
        } catch (error) {
            console.error("Error fetching new recipe:", error);
        }
    }

    async function handleSwapRecipe(originalRecipe: Recipe) {
        if (!token) return;

        setIsLoading(true);

        try {
            const data = await fetchNewRecipe(
                originalRecipe.meal_types[0],
                originalRecipe.recipe_id
            );

            if (!data) return;

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
                                time={msg.time.toLocaleTimeString([], {
                                    hour: "2-digit",
                                    minute: "2-digit",
                                })}
                                text={msg.text}
                                avatar=""
                            />

                            {"sustitution" in msg && msg.sustitution && (
                                <ProposalCard
                                    image={
                                        msg.sustitution.alternative.image_url
                                            ?.split(", ")
                                            .map((img) => img.trim())[0] ?? ""
                                    }
                                    badge="Suggestion"
                                    title={msg.text}
                                    description={`${msg.sustitution.original.name} (${msg.sustitution.original.calories} kcal) → ${msg.sustitution.alternative.name} (${msg.sustitution.alternative.calories} kcal)`}
                                    onConfirm={() =>
                                        setMessages((prev) =>
                                            prev.map((m, idx) =>
                                                idx === i &&
                                                "sustitution" in m
                                                    ? {
                                                          ...m,
                                                          sustitution: {
                                                              ...m.sustitution,
                                                              accepted: true,
                                                          },
                                                      }
                                                    : m
                                            )
                                        )
                                    }
                                    onCancel={() =>
                                        handleSwapRecipe(
                                            msg.sustitution.original
                                        )
                                    }
                                />
                            )}
                        </Fragment>
                    ))}

                    {isLoading && <TypingIndicator />}
                    <div ref={messagesEndRef} />
                </div>

                <ChatInput
                    onSendMessage={handleSendMessage}
                    isLoading={isLoading}
                />
            </div>
        </AppLayout>
    );
}