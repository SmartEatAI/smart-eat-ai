import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/cards/button-card";
import { Check } from "lucide-react";
import { cn } from "@/lib/utils";

interface PlanCardProps {
  title: string;
  price: string;
  description: string;
  features: string[];
  buttonText: string;
  highlighted?: boolean;
}

export default function PlanCard({
  title,
  price,
  description,
  features,
  buttonText,
  highlighted = false,
}: PlanCardProps) {
  return (
    <Card
      className={cn(
        "flex flex-col justify-between",
        highlighted && "border-primary shadow-lg",
      )}
    >
      <div>
        <CardHeader className="text-center space-y-2">
          <CardTitle className="text-xl">{title}</CardTitle>
          <p className="text-3xl font-bold">{price}</p>
          <p className="text-sm text-muted-foreground">{description}</p>
        </CardHeader>

        <CardContent className="space-y-4">
          <ul className="space-y-3">
            {features.map((feature, index) => (
              <li key={index} className="flex gap-2 text-sm">
                <Check className="h-4 w-4 text-primary mt-0.5" />
                <span>{feature}</span>
              </li>
            ))}
          </ul>
        </CardContent>
      </div>

      <div className="p-6 pt-0">
        <Button
          className="w-full"
          variant={highlighted ? "default" : "outline"}
        >
          {buttonText}
        </Button>
      </div>
    </Card>
  );
}
