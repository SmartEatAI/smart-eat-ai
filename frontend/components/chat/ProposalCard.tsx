import { Card, CardContent, CardFooter } from "@/components/ui/card";
import Button from "@/components/ui/button";

interface ProposalCardProps {
    image: string;
    badge: string;
    title: string;
    description?: string;
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
    onConfirm,
    onCancel,
}: ProposalCardProps) {
    return (
        <Card className="w-full overflow-hidden">
            <div className="relative h-40 md:h-52 w-full overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent" />
                <div
                    className="w-full h-full bg-cover bg-center"
                    style={{
                        backgroundImage: `url('${image}')`,
                    }}
                />
                <div className="absolute bottom-3 left-4">
                    <span className="px-2 py-1 rounded text-[10px] font-bold bg-primary text-[#102216] uppercase tracking-wider mb-1 inline-block">
                        {badge}
                    </span>
                    <h3 className="text-white text-lg font-bold">
                        {title}
                    </h3>
                    {description && (
                        <p className="text-gray-200 text-xs mt-1">
                            {description}
                        </p>
                    )}
                </div>
            </div>

            <CardContent className="p-5">
                {/* Contenido adicional puede ir aquí si es necesario */}
            </CardContent>

            <CardFooter className="flex flex-col md:flex-row gap-3 p-5 pt-0">
                <Button
                    onClick={onConfirm}
                    variant="primary"
                    className="w-full md:flex-1 rounded-full py-3 px-4 text-sm font-bold"
                >
                    Confirmar
                </Button>
                <Button
                    onClick={onCancel}
                    variant="secondary"
                    className="w-full md:flex-1 rounded-full py-3 px-4 text-sm font-bold"
                >
                    Cancelar
                </Button>
            </CardFooter>
        </Card>
    );
}
