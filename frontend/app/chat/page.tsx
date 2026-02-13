"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import MessageBubble from "@/components/chat/MessageBubble";
import ProposalCard from "@/components/chat/ProposalCard";
import TypingIndicator from "@/components/chat/TypingIndicator";
import ChatInput from "@/components/chat/ChatInput";

export default function ChatPage() {
  return (
    <AppLayout
      title="Asistente Nutricional Inteligente"
      subtitle="A tu servicio 24/7"
    >
        <div className="flex flex-col gap-4 p-4">
            <MessageBubble
                role="chef"
                time="10:30 AM"
                text="¡Hola! He analizado tu plan actual. ¿Cómo te sientes hoy o qué te gustaría ajustar en tu dieta?"
                avatar="https://placeholder.pics/svg/100"
            />

            <MessageBubble
                role="user"
                time="10:32 AM"
                text="Quiero menos carbohidratos por la noche."
                avatar="https://placeholder.pics/svg/100"
            />

            <div className="flex flex-col gap-2 self-start max-w-[80%]">
                <MessageBubble
                    role="chef"
                    time="10:32 AM"
                    text="Entendido. He encontrado una alternativa deliciosa que reduce tu ingesta de carbohidratos en un 40%. ¿Deseas aplicar el cambio?"
                    avatar="https://placeholder.pics/svg/100"
                />
                <ProposalCard />
            </div>

            <TypingIndicator />

            <ChatInput />
        </div>
    </AppLayout>
  );
}