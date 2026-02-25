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