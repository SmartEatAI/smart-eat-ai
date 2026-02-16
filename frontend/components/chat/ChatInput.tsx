"use client";

import { useState, KeyboardEvent } from "react";
import Button from "@/components/ui/button";

interface ChatInputProps {
  onSendMessage: (message: string) => Promise<void> | void;
  isLoading?: boolean;
}

export default function ChatInput({
  onSendMessage,
  isLoading = false,
}: ChatInputProps) {
  const [message, setMessage] = useState("");

  async function handleSend() {
    const trimmed = message.trim();
    if (!trimmed || isLoading) return;

    await onSendMessage(trimmed);
    setMessage("");
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="sticky bottom-0 left-0 w-full bg-gradient-to-t from-background via-background/95 to-transparent px-4 py-4 md:px-6">
      <div className="mx-auto max-w-4xl">
        <div className="flex items-end gap-2 rounded-2xl border bg-card px-3 py-2 shadow-sm">
          <textarea
            placeholder="Escribe tu mensaje..."
            rows={1}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
            className="flex-1 resize-none bg-transparent text-sm outline-none placeholder:text-muted-foreground md:text-base disabled:opacity-50"
          />

          <Button
            type="button"
            variant="primary"
            onClick={handleSend}
            disabled={isLoading || !message.trim()}
            className="rounded-xl px-4 py-2 text-sm font-medium"
          >
            {isLoading ? "Enviando..." : "Enviar"}
          </Button>
        </div>
      </div>
    </div>
  );
}
