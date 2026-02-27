"use client";

import Image from "next/image";
import { useState, useEffect, useCallback, useRef } from "react";

const FALLBACK = "/images/Image_not_available.png";

interface ImageCarouselProps {
    images: string[];
    alt: string;
    interval?: number;
    className?: string;
}

export default function ImageCarousel({
    images,
    alt,
    interval = 4000,
    className = "relative w-full h-48 bg-muted overflow-hidden",
}: ImageCarouselProps) {
    const srcs = images.length > 0 ? images : [FALLBACK];
    const [activeIdx, setActiveIdx] = useState(0);
    const [imgSrcs, setImgSrcs] = useState<string[]>(srcs);
    const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

    /** Arranca / reinicia el autoplay */
    const startTimer = useCallback(() => {
        if (timerRef.current) clearInterval(timerRef.current);
        if (srcs.length <= 1) return;
        timerRef.current = setInterval(() => {
            setActiveIdx((prev) => (prev + 1) % srcs.length);
        }, interval);
    }, [srcs.length, interval]);

    useEffect(() => {
        startTimer();
        return () => {
            if (timerRef.current) clearInterval(timerRef.current);
        };
    }, [startTimer]);

    /** Navegar manualmente y reiniciar temporizador */
    const goTo = useCallback(
        (idx: number) => {
            setActiveIdx(idx);
            startTimer();
        },
        [startTimer]
    );

    /** Reemplazar imagen rota por fallback */
    const handleError = useCallback((idx: number) => {
        setImgSrcs((prev) => {
            const next = [...prev];
            next[idx] = FALLBACK;
            return next;
        });
    }, []);

    return (
        <div className={className}>
            {/* Imágenes (solo se renderiza la activa para evitar layout shifts) */}
            {imgSrcs.map((src, idx) => (
                <div
                    key={idx}
                    className={`absolute inset-0 transition-opacity duration-500 ${idx === activeIdx ? "opacity-100" : "opacity-0 pointer-events-none"
                        }`}
                >
                    <Image
                        src={src}
                        alt={`${alt} ${idx + 1}`}
                        fill
                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                        className="object-cover"
                        quality={90}
                        priority={idx === 0}
                        onError={() => handleError(idx)}
                    />
                </div>
            ))}

            {/* Dots — solo si hay más de una imagen */}
            {imgSrcs.length > 1 && (
                <div className="absolute bottom-2 left-0 right-0 flex justify-center gap-1.5 z-10">
                    {imgSrcs.map((_, idx) => (
                        <button
                            key={idx}
                            aria-label={`Imagen ${idx + 1}`}
                            onClick={() => goTo(idx)}
                            className={`rounded-full transition-all duration-300 ${idx === activeIdx
                                    ? "w-4 h-2 bg-white"
                                    : "w-2 h-2 bg-white/50 hover:bg-white/80"
                                }`}
                        />
                    ))}
                </div>
            )}
        </div>
    );
}
