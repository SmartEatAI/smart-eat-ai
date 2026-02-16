"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import ProtectedRoute from "@/components/auth/ProtectedRoute";

function MyPlanPage() {
  return (
    <AppLayout
      title="Mi Plan Nutricional"
      subtitle="Tu plan personalizado"
    >
      <div className="p-6 rounded-xl border">
        Info page
      </div>
    </AppLayout>
  );
}

export default function MyPlanPageWrapper() {
  return (
    <ProtectedRoute>
      <MyPlanPage />
    </ProtectedRoute>
  );
}