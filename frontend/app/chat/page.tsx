"use client";

import { useRef, useEffect, useState, Fragment } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import MessageBubble from "@/components/chat/MessageBubble";
import ProposalCard from "@/components/chat/ProposalCard";
import TypingIndicator from "@/components/chat/TypingIndicator";
import ChatInput from "@/components/chat/ChatInput";

type Message = {
    role: "user" | "chef";
    text: string;
    time: string;
    sustitution?: {
        original: {
            name: string;
            info: string;
        };
        alternative: {
            name: string;
            info: string;
        };
    };
};

export default function ChatPage() {

    const messagesEndRef = useRef<HTMLDivElement>(null);

    const [messages, setMessages] = useState<Message[]>([
        {
            role: "chef",
            time: "10:30 AM",
            text: "¡Hola! He analizado tu plan actual. ¿Cómo te sientes hoy o qué te gustaría ajustar en tu dieta?",
        },
        {
            role: "user",
            time: "10:31 AM",
            text: "Quiero menos carbohidratos por la noche.",
        },
        {
            role: "chef",
            time: "10:32 AM",
            text: "Entiendo. Te recomendaré una cena con menos carbohidratos.",
        },
        {
            role: "chef",
            time: "10:33 AM",
            text: "Sustitución de Cena",
            sustitution: {
                original: {
                    name: "Pasta Alfredo",
                    info: "850 kcal - 90g Carbs",
                },
                alternative: {
                    name: "Ensalada de Pollo",
                    info: "450 kcal - 20g Carbs",
                }
            }
        }
    ]);

    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    async function handleSendMessage(message: string) {
        // Añadir mensaje del usuario
        const userMessage: Message = {
            role: "user",
            text: message,
            time: new Date().toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
            }),
        };

        setMessages((prev) => [...prev, userMessage]);
        setIsLoading(true);

        try {
            // Llamada a tu API
            const res = await fetch("/api/chat", {
                method: "POST",
                body: JSON.stringify({ message }),
            });

            const data = await res.json();

            const assistantMessage: Message = {
                role: "chef",
                text: data.reply || "Respuesta del asistente",
                time: new Date().toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                }),
            };

            setMessages((prev) => [...prev, assistantMessage]);
        } catch (error) {
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <AppLayout
            title="Asistente Nutricional Inteligente"
            subtitle="A tu servicio 24/7"
        >
            <div className="flex flex-col h-[80vh]">
                {/* Zona de mensajes */}
                <div className="flex-1 flex flex-col gap-4 p-4">
                    {messages.map((msg, i) => (
                        <Fragment key={i}>
                            <MessageBubble
                                role={msg.role}
                                time={msg.time}
                                text={msg.text}
                                avatar=""
                            />

                            {msg.sustitution && (
                                <ProposalCard
                                    image="https://lh3.googleusercontent.com/aida-public/AB6AXuBqC_uQaB_fCsD_B-BhOvy8WfnUufREXINi5-vsMZVx4xYpICl_DIRq61843DMZRXmux9ewS5ABOqCCmQkuHaWEl_JqndFWcrFv_YRlP_NBfTlpXjG5STtMS7sc-YIMcsk9X9M_DOUakZzbIBvHBzxxv3rG9NZjlq9KRryQrOQB1ssZNPlP_GFUZCy32l0P7fs40R2YIj6wLpJeP-AGlRH7txJGqWfZNV30MSqZodnTJIxR5d1KmwOuHE1q-BLTyRgHcCNFEK42EUAP"
                                    badge="Sugerencia"
                                    title={msg.text}
                                    description={`${msg.sustitution.original.name} (${msg.sustitution.original.info}) -> ${msg.sustitution.alternative.name} (${msg.sustitution.alternative.info})`}
                                    onConfirm={() => console.log("Propuesta confirmada")}
                                    onCancel={() => console.log("Propuesta cancelada")}
                                />
                            )}
                        </Fragment>
                    ))}

                    {isLoading && <TypingIndicator />}

                    <div ref={messagesEndRef} />
                </div>

                {/* Input fijo abajo */}
                <ChatInput
                    onSendMessage={handleSendMessage}
                    isLoading={isLoading}
                />
            </div>
        </AppLayout>
    );
}
