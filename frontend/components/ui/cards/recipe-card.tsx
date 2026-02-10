"use client";

import Image from "next/image";

interface RecipeCardProps {
  title: string;
  calories: number;
  image: string;
}

export default function RecipeCard({ title, calories, image }: RecipeCardProps) {
  return (
    <div className="border rounded-lg overflow-hidden shadow-md">
      <Image
        src={image}
        alt={title}
        width={300}
        height={200}
        className="w-full h-40 object-cover"
      />
      <div className="p-4">
        <h3 className="text-lg font-semibold mb-2">{title}</h3>
        <p className="text-sm text-muted-foreground">{calories} kcal</p>
      </div>
    </div>
  );
}