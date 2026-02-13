export default function ChatInput() {
    return (
        <div className="absolute bottom-0 left-0 w-full p-4 md:p-6 bg-gradient-to-t from-background-light dark:from-background-dark via-background-light dark:via-background-dark to-transparent">
            <div className="max-w-4xl mx-auto">
                <div className="flex items-center gap-2 p-2 pr-2 bg-surface-light dark:bg-surface-dark rounded-full border">
                    <input
                        className="flex-1 bg-transparent border-none focus:ring-0 text-sm md:text-base"
                        placeholder="Escribe tu mensaje..."
                        type="text"
                    />
                    <button className="p-3 rounded-full bg-primary text-[#102216]">
                        Enviar
                    </button>
                </div>
            </div>
        </div>
    );
}
