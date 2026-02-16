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
        // Check if user is already authenticated
        const token = localStorage.getItem("token");
        const user = localStorage.getItem("user");

        if (token && user) {
            // Already authenticated, redirect to dashboard
            router.push("/dashboard");
        } else {
            // Not authenticated, allow access
            setIsChecking(false);
        }
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
