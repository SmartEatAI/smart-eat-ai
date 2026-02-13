export default function TypingIndicator() {
    return (
        <div className="flex items-end gap-3 self-start max-w-[90%] opacity-50">
            <div className="w-8 h-8 rounded-full bg-gray-400" />
            <div className="p-3 rounded-2xl rounded-tl-none bg-surface-dark flex gap-1">
                <span className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" />
                <span className="w-2 h-2 rounded-full bg-gray-400 animate-bounce [animation-delay:0.1s]" />
                <span className="w-2 h-2 rounded-full bg-gray-400 animate-bounce [animation-delay:0.2s]" />
            </div>
        </div>
    );
}
