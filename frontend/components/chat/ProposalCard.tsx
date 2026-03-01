import { Card, CardFooter } from "@/components/ui/card";
import Button from "@/components/ui/Button";
import ImageCarousel from "../ui/ImageCarousel";

interface ProposalCardProps {
    image: string;
    badge: string;
    title: string;
    description?: string;
    extraInfo?: React.ReactNode;
    confirmText?: string;
    cancelText?: string;
    onConfirm?: () => void;
    onCancel?: () => void;
}

export default function ProposalCard({
    image,
    badge,
    title,
    description,
    extraInfo,
    confirmText = "Confirm",
    cancelText = "Cancel",
    onConfirm,
    onCancel,
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
            <div className="p-5 flex flex-col gap-2">
                {/* Badge */}
                <span className="px-3 py-1 rounded-full text-xs font-bold bg-primary text-[#102216] uppercase tracking-wider inline-block mb-2">
                    {badge}
                </span>

                {/* Título */}
                <h3 className="text-lg font-semibold line-clamp-2 text-foreground">{title}</h3>

                {/* Descripción / macros */}
                {description && (
                    <p className="text-sm text-muted-foreground line-clamp-2">{description}</p>
                )}

                {/* Extra info (ej: botón "Otra receta") */}
                {extraInfo}
            </div>

            {/* Botones */}
            <CardFooter className="flex flex-col sm:flex-row gap-3 p-4">
                <Button
                    onClick={onConfirm}
                    variant="primary"
                    className="w-full rounded-full py-2 px-4 text-sm font-semibold"
                >
                    {confirmText}
                </Button>
                <Button
                    onClick={onCancel}
                    variant="secondary"
                    className="w-full rounded-full py-2 px-4 text-sm font-semibold"
                >
                    {cancelText}
                </Button>
            </CardFooter>
        </Card>
    );
}