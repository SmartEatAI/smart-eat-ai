import { Utensils } from "lucide-react";
import Button from "@/components/ui/Button";
import { useRouter } from "next/navigation";

export default function NoPlanCard() {
    const router = useRouter();
    return (
        <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
            <div className="bg-card/50 rounded-full p-6 mb-6">
                <Utensils className="w-16 h-16 text-muted-foreground" />
            </div>
            <h3 className="text-2xl font-semibold text-primary mb-3">
                No Active Nutrition Plan
            </h3>
            <p className="text-muted-foreground max-w-md mb-8">
                You don't have an active nutrition plan yet. Create a personalized plan by chatting with our AI nutritionist!
            </p>
            <Button
                variant="primary"
                size="lg"
                onClick={() => router.push("/chat")}
                className="shadow-lg"
            >
                Create Your Plan
            </Button>
        </div>
    );
}
