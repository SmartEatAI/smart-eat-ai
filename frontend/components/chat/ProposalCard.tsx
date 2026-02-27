import { Card, CardContent, CardFooter } from "@/components/ui/card";
import Button from "@/components/ui/Button";

interface ProposalCardProps {
    image: string;
    badge: string;
    title: string;
    description?: string;
    extraInfo?: React.ReactNode;
    confirmText?: string;
    cancelText?: string;
    onConfirm?: () => void; // → llama a handleConfirm (guarda en API + actualiza estado)
    onCancel?: () => void;  // → llama a setProposal(null) (descarta la propuesta)
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
        <Card className="w-full min-w-[220px] max-w-[350px] min-h-[345px] border rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 bg-card flex flex-col">
            {/* Imagen con Badge */}
            <div className="relative h-40 md:h-52 w-full flex-shrink-0 flex-grow">
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent" />
                <div
                    className="w-full h-full bg-cover bg-center"
                    style={{
                        backgroundImage: `url('${image}')`,
                    }}
                />
                <div className="absolute bottom-4 left-4 right-4">
                    <span className="px-3 py-1 rounded-full text-xs font-bold bg-primary text-[#102216] uppercase tracking-wider inline-block mb-2">
                        {badge}
                    </span>
                    <h3 className="text-white text-lg font-bold line-clamp-2">
                        {title}
                    </h3>
                    {description && (
                        <p className="text-gray-200 text-xs mt-2 line-clamp-2">
                            {description}
                        </p>
                    )}
                    {extraInfo}
                </div>
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