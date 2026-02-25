"use client";

import { ReactNode } from "react";
import ImageCarousel from "@/components/ui/ImageCarousel";

interface RecipeCardProps {
  title: string;
  calories: number;
  images: string[];
  children?: ReactNode;
}

export default function RecipeCard({ title, calories, images, children }: RecipeCardProps) {
  return (
    <div className="border rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 bg-card">
      <ImageCarousel images={images} alt={title} />
      <div className="p-5">
        <h3 className="text-lg font-semibold mb-2 line-clamp-1 text-foreground">{title}</h3>
        <p className="text-sm text-muted-foreground font-medium">{calories} kcal</p>
        {children && <div className="mt-4">{children}</div>}
      </div>
    </div>
  );
}