"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import ProtectedRoute from "@/components/auth/ProtectedRoute";

function ProfilePage() {
  return (
    <AppLayout
      title="Mi Perfil"
      subtitle="Información personal"
    >
      <div className="p-6 rounded-xl border">
        Info page
      </div>
    </AppLayout>
  );
}

export default function ProfilePageWrapper() {
  return (
    <ProtectedRoute>
      <ProfilePage />
    </ProtectedRoute>
  );
}