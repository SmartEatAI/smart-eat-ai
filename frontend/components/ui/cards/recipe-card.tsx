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
  mealType?: string | { name?: string } | Array<string | { name?: string }>;
  images: string;
  recipeUrl?: string;
  children?: ReactNode;
}

export default function RecipeCard({ title, calories, protein, carbs, fats, mealType, images, recipeUrl, children }: RecipeCardProps) {
  // Debug: log mealType prop and its type
  if (typeof window !== "undefined") {
     
  }

  // Función para formatear el mealType (ej: "breakfast" → "Breakfast")
  const formatMealType = (type: string) => {
    if (!type) return "";
    return type.charAt(0).toUpperCase() + type.slice(1);
  };

  let mealTypeBadges: string[] = [];
  if (Array.isArray(mealType)) {
    mealTypeBadges = mealType
      .map((mt: any) => {
        if (typeof mt === "string") return formatMealType(mt);
        if (mt && typeof mt === "object" && "name" in mt && typeof mt.name === "string") return formatMealType(mt.name);
        return null;
      })
      .filter((mt): mt is string => Boolean(mt && mt.trim() !== ""));
  } else if (typeof mealType === "string" && mealType) {
    mealTypeBadges = [formatMealType(mealType)];
  } else if (mealType && typeof mealType === "object" && "name" in mealType && typeof (mealType as any).name === "string") {
    mealTypeBadges = [formatMealType((mealType as any).name)];
  }

  const imageArray: string[] = images
  ? images.split(', ').map(img => img.trim())
  : [];

  return (
    <div className="border rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 bg-card">
      <ImageCarousel images={imageArray} alt={title} />
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
        {/* Meal Type - badge style */}
        {mealTypeBadges.length > 0 && (
          <div className="flex flex-wrap gap-1 mb-2">
            {mealTypeBadges.map((badge, idx) => (
              <span
                key={idx}
                className="inline-block bg-primary/10 text-primary text-xs font-semibold px-2 py-0.5 rounded-full border border-primary/20 tracking-wide"
              >
                {badge}
              </span>
            ))}
          </div>
        )}
        {/* Macros info */}
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