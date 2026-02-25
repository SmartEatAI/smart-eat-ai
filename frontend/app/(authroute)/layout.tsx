"use client";

import React from "react";
import { useAuth } from "@/hooks/useAuth";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
	const { user, loading } = useAuth();

	if (loading) {
		return <div className="flex items-center justify-center min-h-screen">Cargando...</div>;
	}

	if (user) {
		return (
			<div className="flex items-center justify-center min-h-screen">
				<div className="bg-white p-8 rounded shadow text-center">
					<h2 className="text-xl font-bold mb-4">Acceso restringido</h2>
					<p>Por favor, cierra sesión para acceder a esta área.</p>
				</div>
			</div>
		);
	}

	return <>{children}</>;
}
