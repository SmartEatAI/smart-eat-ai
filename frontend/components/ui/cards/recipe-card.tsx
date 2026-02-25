"use client";

import Image from "next/image";
import { ReactNode, useState } from "react";

interface RecipeCardProps {
  title: string;
  calories: number;
  image: string;
  children?: ReactNode;
}


export default function RecipeCard({ title, calories, image, children }: RecipeCardProps) {
  const [imgSrc, setImgSrc] = useState(image);

  return (
    <div className="border rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 bg-card">
      <div className="relative w-full h-48 overflow-hidden bg-muted">
        <Image
          src={imgSrc}
          alt={title}
          fill
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          className="object-cover hover:scale-110 transition-transform duration-500"
          quality={95}
          priority={false}
          onError={() => setImgSrc("/images/Image_not_available.png")}
        />
      </div>
      <div className="p-5">
        <h3 className="text-lg font-semibold mb-2 line-clamp-1 text-foreground">{title}</h3>
        <p className="text-sm text-muted-foreground font-medium">{calories} kcal</p>
        {children && <div className="mt-4">{children}</div>}
      </div>
    </div>
  );
}