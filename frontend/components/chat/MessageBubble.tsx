import { MessageBubbleProps } from "@/types/chat";

export default function MessageBubble({
    role,
    time,
    text,
    avatar,
}: MessageBubbleProps) {
    const isUser = role === "user";

    return (
        <div
            className={`flex items-end gap-3 ${isUser ? "self-end flex-row-reverse" : "self-start"} w-full max-w-full md:max-w-[70%]`}
        >
            <div
                className={`bg-cover bg-center rounded-full w-10 h-10 shrink-0 ${isUser ? "border-2 border-primary" : "border border-gray-700"
                    }`}
                style={{ backgroundImage: `url(${avatar})` }}
            />

            <div
                className={`flex flex-col gap-1 ${isUser ? "items-end" : "items-start"
                    }`}
            >
                <span className="text-gray-500 dark:text-[#9db9a6] text-[11px] font-medium">
                    {isUser ? "You" : "SmartEatAI Chef"} • {time}
                </span>

                <div
                    className={`p-3 md:p-4 rounded-2xl shadow-sm break-words ${isUser
                        ? "rounded-tr-none bg-primary text-[#111813]"
                        : "rounded-tl-none bg-green-950/70 text-primary border border-green-900"}`}
                >
                    <p className="text-sm md:text-base leading-relaxed">{text}</p>
                </div>
            </div>
        </div>
    );
}
