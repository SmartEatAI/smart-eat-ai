import { cn } from "@/lib/utils";

interface StepProps {
  number: string;
  title: string;
  description: string;
  variant: "outline" | "muted";
}

export default function Step({ number, title, description, variant }: StepProps) {
  return (
    <div className="flex gap-4 items-start">
      <div
        className={cn(
          "flex h-10 w-10 shrink-0 items-center justify-center rounded-full text-sm font-bold",
          variant === "outline" &&
            "border border-primary text-primary bg-transparent",
          variant === "muted" &&
            "bg-muted text-foreground"
        )}
      >
        {number}
      </div>

      <div>
        <h3 className="font-semibold text-lg">
          {title}
        </h3>
        <p className="text-sm text-muted-foreground mt-1">
          {description}
        </p>
      </div>
    </div>
  );
}