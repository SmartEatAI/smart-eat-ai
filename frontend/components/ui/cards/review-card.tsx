import { Card, CardContent } from "@/components/ui/card";
import { Star } from "lucide-react";
import Image from "next/image";

interface ReviewCardProps {
  name: string;
  image: string;
  rating: number;
  review: string;
}

export default function ReviewCard({ name, image, rating, review }: ReviewCardProps) {
  return (
    <Card className="h-full">
      <CardContent className="p-6 flex flex-col gap-4">

        {/* Header */}
        <div className="flex items-center gap-4">
          <Image
            src={image}
            alt={name}
            width={48}
            height={48}
            className="rounded-full object-cover"
          />

          <div>
            <p className="font-semibold text-sm">
              {name}
            </p>
            <div className="flex gap-1">
              {Array.from({ length: 5 }).map((_, i) => (
                <Star
                  key={i}
                  className={`h-4 w-4 ${
                    i < rating
                      ? "fill-primary text-primary"
                      : "text-muted-foreground"
                  }`}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Review */}
        <p className="text-sm text-muted-foreground leading-relaxed">
          “{review}”
        </p>

      </CardContent>
    </Card>
  );
}