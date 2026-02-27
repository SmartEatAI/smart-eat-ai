"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";

interface ProtectedRouteProps {
    children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
    const router = useRouter();
    const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
    const { user, token } = useAuth();
    
    useEffect(() => {
        const validateToken = async () => {
            if (!token || !user) {
                // Not authenticated, redirect to auth page
                router.push("/auth");
                return;
            }

            try {
                // Validate token with backend
                const response = await fetch("http://localhost:8000/api/auth/me", {
                    headers: {
                        "Authorization": `Bearer ${token}`,
                    },
                });

                if (!response.ok) {
                    // Token is invalid or expired
                    localStorage.removeItem("token");
                    localStorage.removeItem("user");
                    router.push("/auth");
                    return;
                }

                // Token is valid
                const userData = await response.json();
                // Optionally update user data in localStorage
                localStorage.setItem("user", JSON.stringify(userData));
                setIsAuthenticated(true);
            } catch (error) {
                console.error("Token validation error:", error);
                localStorage.removeItem("token");
                localStorage.removeItem("user");
                router.push("/auth");
            }
        };

        validateToken();
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
