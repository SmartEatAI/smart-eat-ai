import Button from "@/components/ui/button";

export default function ChatInput() {
  return (
    <div className="sticky bottom-0 left-0 w-full bg-gradient-to-t from-background via-background/95 to-transparent px-4 py-4 md:px-6">
      <div className="mx-auto max-w-4xl">
        <div className="flex items-end gap-2 rounded-2xl border bg-card px-3 py-2 shadow-sm">
          <textarea
            placeholder="Escribe tu mensaje..."
            rows={1}
            className="flex-1 resize-none bg-transparent text-sm outline-none placeholder:text-muted-foreground md:text-base"
          />

          <Button
            type="button"
            variant="primary"
            className="rounded-xl px-4 py-2 text-sm font-medium"
          >
            Enviar
          </Button>
        </div>
      </div>
    </div>
  );
}
