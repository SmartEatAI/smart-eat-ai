"use client";

import { useProfileContext } from "@/context/ProfileContext";
import { useRouter, usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import Toast from "@/components/ui/Toast";

export default function ProfileGuard({ children }: { children: React.ReactNode }) {
  const { hasProfile, loading } = useProfileContext();
  const router = useRouter();
  const pathname = usePathname();
  const [showToast, setShowToast] = useState(false);
  const [redirecting, setRedirecting] = useState(false);

  // Rutas que no requieren perfil creado
  const PUBLIC_PATHS = ["/auth", "/profile"];

  const isPublicPath = PUBLIC_PATHS.includes(pathname);

  useEffect(() => {
    // No hacer nada mientras carga o en rutas públicas
    if (loading || isPublicPath) return;

    if (hasProfile === false) {
      setShowToast(true);
      setRedirecting(true);
      router.push("/profile");
    }
  }, [hasProfile, loading, isPublicPath, router]);

  // Reiniciar redirecting cuando llegamos a /profile
  useEffect(() => {
    if (isPublicPath) {
      setRedirecting(false);
    }
  }, [isPublicPath]);

  // Mostrar spinner global mientras se verifica el perfil (solo en rutas protegidas)
  if ((loading || redirecting) && !isPublicPath) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-primary text-lg">Loading...</p>
        </div>
        {showToast && (
          <Toast
            message="Rellene su perfil para continuar"
            type="error"
            onClose={() => setShowToast(false)}
          />
        )}
      </div>
    );
  }

  return (
    <>
      {showToast && (
        <Toast
          message="Rellene su perfil para continuar"
          type="error"
          onClose={() => setShowToast(false)}
        />
      )}
      {children}
    </>
  );
}