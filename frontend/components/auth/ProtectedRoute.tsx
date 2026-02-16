"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

interface ProtectedRouteProps {
    children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
    const router = useRouter();
    const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

    useEffect(() => {
        // Check if user is authenticated
        const token = localStorage.getItem("token");
        const user = localStorage.getItem("user");

        if (!token || !user) {
            // Not authenticated, redirect to auth page
            router.push("/auth");
        } else {
            // Authenticated
            setIsAuthenticated(true);
        }
    }, [router]);

    // Show loading state while checking authentication
    if (isAuthenticated === null) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-background">
                <div className="text-center">
                    <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-primary text-lg">Loading...</p>
                </div>
            </div>
        );
    }

    // If authenticated, render children
    return <>{children}</>;
};

export default ProtectedRoute;
