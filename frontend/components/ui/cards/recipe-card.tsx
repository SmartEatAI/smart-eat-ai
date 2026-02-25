"use client";

import { ReactNode } from "react";
import { Info } from "lucide-react";
import ImageCarousel from "@/components/ui/ImageCarousel";

interface RecipeCardProps {
  title: string;
  calories: number;
  protein?: number;
  carbs?: number;
  fats?: number;
  images: string[];
  recipeUrl?: string;
  children?: ReactNode;
}

export default function RecipeCard({ title, calories, protein, carbs, fats, images, recipeUrl, children }: RecipeCardProps) {
  return (
    <div className="border rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 bg-card">
      <ImageCarousel images={images} alt={title} />
      <div className="p-5">
        <div className="flex items-start justify-between gap-2 mb-2">
          <h3 className="text-lg font-semibold line-clamp-1 text-foreground">{title}</h3>
          {recipeUrl && (
            <a
              href={recipeUrl}
              target="_blank"
              rel="noopener noreferrer"
              aria-label={`More info about ${title}`}
              className="shrink-0 text-muted-foreground hover:text-primary transition-colors"
            >
              <Info className="size-5" />
            </a>
          )}
        </div>
        <p className="text-sm text-muted-foreground font-medium">
          {calories} kcal
          {typeof protein === "number" && typeof carbs === "number" && typeof fats === "number" && (
            <>
              {" "}
              • {protein}g Prot • {carbs}g Carb • {fats}g Fat
            </>
          )}
        </p>
        {children && <div className="mt-4">{children}</div>}
      </div>
    </div>
  );
}