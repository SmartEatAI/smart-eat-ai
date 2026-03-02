import { Card, CardFooter } from "@/components/ui/card";
import { Check, X, RefreshCw, Info } from "lucide-react";
import ImageCarousel from "../ui/ImageCarousel";

interface ProposalCardProps {
    image: string;
    badge: string;
    title: string;
    description?: string;
    onAnother?: () => void;
    confirmText?: string;
    cancelText?: string;
    onConfirm?: () => void;
    calories?: number;
    protein?: number;
    carbs?: number;
    fats?: number;
    recipeUrl?: string;
    onCancel?: () => void;
}

export default function ProposalCard({
    image,
    badge,
    title,
    description,
    onAnother,
    confirmText = "Confirm",
    cancelText = "Cancel",
    onConfirm,
    onCancel,
    calories,
    protein,
    carbs,
    fats,
    recipeUrl,
}: ProposalCardProps) {
    return (
        <Card className="border rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 bg-card flex flex-col">
            {/* Imagen / Carousel */}
            <ImageCarousel 
            key={image}
            images={
                image
                    ? image.includes(", ")
                        ? image.split(", ").map(img => img.trim())
                        : [image.trim()]
                    : []
            } alt={title} />

            {/* Contenido */}
            <div className="p-5 flex flex-col">
                {/* Badge */}

                {/* Badge + Info */}

                                <div className="flex items-center justify-between mb-2 w-full">
                                    <span className="px-3 py-0.5 rounded-full text-xs font-bold bg-primary text-[#102216] uppercase tracking-wider max-w-[160px] truncate">
                                        {badge}
                                    </span>
                                    {recipeUrl ? (
                                        <a
                                            href={recipeUrl}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            aria-label={`More info about ${title}`}
                                            className="shrink-0 text-muted-foreground hover:text-primary transition-colors flex items-center"
                                        >
                                            <Info className="size-5" />
                                        </a>
                                    ) : (
                                        <span className="flex items-center">
                                            <Info className="size-5 text-muted-foreground" />
                                        </span>
                                    )}
                                </div>

                {/* Título */}
                <h3 className="text-lg font-semibold line-clamp-1 text-foreground">{title}</h3>

                {/* Macros info */}
                {(typeof calories === "number") && (
                    <p className="text-sm text-muted-foreground font-medium">
                        {calories} kcal
                        {typeof protein === "number" && typeof carbs === "number" && typeof fats === "number" && (
                        <>
                            {" "}
                            • {protein}g Prot • {carbs}g Carb • {fats}g Fat
                        </>
                        )}
                    </p>
                )}

            </div>

            {/* Iconos de acción */}
            <CardFooter className="flex flex-row items-center justify-center gap-6">
                <button
                    onClick={onConfirm}
                    className="flex flex-col items-center justify-center text-greenree-500 hover:text-green-600 transition-colors focus:outline-none"
                    title={confirmText}
                >
                    <Check className="w-5 h-5" />
                    <span className="text-xs mt-1">{confirmText}</span>
                </button>
                {onAnother && (
                    <button
                        onClick={onAnother}
                        className="flex flex-col items-center justify-center text-primary hover:text-green-500 transition-colors focus:outline-none"
                        title="Another suggestion"
                    >
                        <RefreshCw className="w-5 h-5" />
                        <span className="text-xs mt-1">Change</span>
                    </button>
                )}
                <button
                    onClick={onCancel}
                    className="flex flex-col items-center justify-center text-greenree-400 hover:text-red-500 transition-colors focus:outline-none"
                    title={cancelText}
                >
                    <X className="w-5 h-5" />
                    <span className="text-xs mt-1">{cancelText}</span>
                </button>
            </CardFooter>
        </Card>
    );
}