"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

interface PublicRouteProps {
    children: React.ReactNode;
}

const PublicRoute: React.FC<PublicRouteProps> = ({ children }) => {
    const router = useRouter();
    const [isChecking, setIsChecking] = useState(true);

    useEffect(() => {
        const checkAuthentication = async () => {
            const token = localStorage.getItem("token");
            const user = localStorage.getItem("user");

            if (!token || !user) {
                // Not authenticated, allow access to public route
                setIsChecking(false);
                return;
            }

            try {
                // Validate token with backend
                const response = await fetch("http://localhost:8000/api/auth/me", {
                    headers: {
                        "Authorization": `Bearer ${token}`,
                    },
                });

                if (response.ok) {
                    // Token is valid, user is authenticated, redirect to dashboard
                    router.push("/dashboard");
                } else {
                    // Token is invalid, clean up and allow access to public route
                    localStorage.removeItem("token");
                    localStorage.removeItem("user");
                    setIsChecking(false);
                }
            } catch (error) {
                console.error("Token validation error:", error);
                // On error, clean up and allow access to public route
                localStorage.removeItem("token");
                localStorage.removeItem("user");
                setIsChecking(false);
            }
        };

        checkAuthentication();
    }, [router]);

    // Show loading state while checking authentication
    if (isChecking) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-background">
                <div className="text-center">
                    <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-primary text-lg">Loading...</p>
                </div>
            </div>
        );
    }

    // If not authenticated, render children
    return <>{children}</>;
};

export default PublicRoute;
