"use client";

import { AppLayout } from "@/components/layout/AppLayout";

export default function ProfilePage() {
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