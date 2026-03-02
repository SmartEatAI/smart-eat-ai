import React from "react";
import { ProfileProvider } from "@/context/ProfileContext";
import ProtectedRoute from "@/components/auth/ProtectedRoute";
import ProfileGuard from "@/components/auth/ProfileGuard";
import { AuthProvider } from "@/context/AuthContext";

export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <ProtectedRoute>
        <ProfileProvider>
          <ProfileGuard>
            {children}
          </ProfileGuard>
        </ProfileProvider>
      </ProtectedRoute>
    </AuthProvider>
  );
}
