"use client";

import { useRef, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import MessageBubble from "@/components/chat/MessageBubble";
import ProposalCard from "@/components/chat/ProposalCard";
import TypingIndicator from "@/components/chat/TypingIndicator";
import ChatInput from "@/components/chat/ChatInput";

export default function ChatPage() {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  return (
    <AppLayout
      title="Asistente Nutricional Inteligente"
      subtitle="A tu servicio 24/7"
    >
        <div className="flex flex-col gap-4 p-4 lg:px-20">
            <MessageBubble
                role="chef"
                time="10:30 AM"
                text="¡Hola! He analizado tu plan actual. ¿Cómo te sientes hoy o qué te gustaría ajustar en tu dieta?"
                avatar=""
            />

            <MessageBubble
                role="user"
                time="10:32 AM"
                text="Quiero menos carbohidratos por la noche."
                avatar=""
            />

            <div className="flex flex-col gap-2 self-start max-w-[80%] md:max-w-md lg:max-w-lg">
                <MessageBubble
                    role="chef"
                    time="10:32 AM"
                    text="Entendido. He encontrado una alternativa deliciosa que reduce tu ingesta de carbohidratos en un 40%. ¿Deseas aplicar el cambio?"
                    avatar=""
                />
                <ProposalCard
                    image="https://lh3.googleusercontent.com/aida-public/AB6AXuBqC_uQaB_fCsD_B-BhOvy8WfnUufREXINi5-vsMZVx4xYpICl_DIRq61843DMZRXmux9ewS5ABOqCCmQkuHaWEl_JqndFWcrFv_YRlP_NBfTlpXjG5STtMS7sc-YIMcsk9X9M_DOUakZzbIBvHBzxxv3rG9NZjlq9KRryQrOQB1ssZNPlP_GFUZCy32l0P7fs40R2YIj6wLpJeP-AGlRH7txJGqWfZNV30MSqZodnTJIxR5d1KmwOuHE1q-BLTyRgHcCNFEK42EUAP"
                    badge="Sugerencia"
                    title="Sustitución de Cena"
                    description="-40% carbohidratos"
                    confirmText="Confirmar"
                    cancelText="Cancelar"
                    onConfirm={() => console.log("Propuesta confirmada")}
                    onCancel={() => console.log("Propuesta cancelada")}
                />
            </div>

            <TypingIndicator />

            <div ref={messagesEndRef} />
            <ChatInput />
        </div>
    </AppLayout>
  );
}