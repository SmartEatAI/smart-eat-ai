"use client";

import Button from "@/components/ui/Button";
import { usePathname, useRouter } from "next/navigation";
import { cn } from "@/lib/utils";
import { LogOut, ChevronLeft, ChevronRight, LayoutDashboard, ClipboardList, Menu, X, MessagesSquare, UserRoundPen } from "lucide-react";
import { useState } from "react";

const links = [
    { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { href: "/my-plan", label: "My Plan", icon: ClipboardList },
    { href: "/chat", label: "Chat", icon: MessagesSquare },
    { href: "/profile", label: "Profile", icon: UserRoundPen },
];

interface SidebarProps {
    className?: string;
}

const Sidebar: React.FC<SidebarProps> = ({ className }) => {
    const pathname = usePathname();
    const router = useRouter();
    const [isOpen, setIsOpen] = useState(true);
    const [isMobileOpen, setIsMobileOpen] = useState(false);

    const handleLogout = () => {
        // Remove token and user data from localStorage
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        // Redirect to landing page
        router.push("/");
    };

    return (
        <>
            {/* Botón toggle para mobile - Solo muestra cuando está cerrado */}
            {!isMobileOpen && (
                <button
                    className="fixed top-4 left-4 z-50 p-2.5 bg-background text-primary rounded-full shadow-lg hover:bg-secondary transition-all duration-300 md:hidden"
                    onClick={() => setIsMobileOpen(true)}
                    aria-label="Toggle menu"
                >
                    <Menu className="h-5 w-5" />
                </button>
            )}

            {/* Overlay para mobile */}
            {isMobileOpen && (
                <div
                    className="fixed inset-0 bg-black bg-opacity-50 z-30 md:hidden"
                    onClick={() => setIsMobileOpen(false)}
                />
            )}

            {/* Sidebar */}
            <aside
                className={cn(
                    "bg-card text-secondary-foreground h-screen p-4 flex flex-col justify-between transition-all duration-300",
                    // Mobile: fixed y oculto por defecto
                    "fixed top-0 left-0 z-40",
                    isMobileOpen ? "translate-x-0" : "-translate-x-full",
                    "md:translate-x-0 md:relative",
                    // Desktop: ancho variable
                    isOpen ? "w-64 md:w-64" : "w-64 md:w-16 md:p-2",
                    className // Apply the passed className
                )}
            >
                {/* Header con botón toggle y logo */}
                <div className={cn(
                    "flex mb-4 transition-all duration-300 items-center",
                    isOpen ? "justify-between" : "justify-between md:justify-center"
                )}>
                    {/* Logo - siempre visible en móvil cuando está abierto, en desktop según isOpen */}
                    {(isMobileOpen || isOpen) && (
                        <span
                            className={cn(
                                "font-bold text-primary cursor-pointer",
                                "text-lg md:text-xl" // Texto más pequeño en móvil
                            )}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.textShadow =
                                    "0 0 10px rgba(72,187,120,0.8), 0 0 20px rgba(72,187,120,0.6)";
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.textShadow = "none";
                            }}
                        >
                            🥗 SmartEatAI
                        </span>
                    )}
                    
                    {/* Botón de cerrar para móvil / toggle para desktop */}
                    <button
                        className="p-2.5 bg-background text-primary rounded-full shadow-lg hover:bg-secondary transition-all duration-300"
                        onClick={() => {
                            if (window.innerWidth < 768) {
                                setIsMobileOpen(false);
                            } else {
                                setIsOpen(!isOpen);
                            }
                        }}
                        aria-label="Toggle sidebar"
                    >
                        {/* En móvil muestra X, en desktop muestra chevron */}
                        <span className="md:hidden">
                            <X className="h-4 w-4" />
                        </span>
                        <span className="hidden md:block">
                            {isOpen ? <ChevronLeft className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
                        </span>
                    </button>
                </div>

                <nav className="space-y-4">
                    {links.map((link) => {
                        const Icon = link.icon;
                        return (
                            <Button
                                key={link.href}
                                as="a"
                                href={link.href}
                                variant={pathname === link.href ? "primary" : "secondary"}
                                className={cn(
                                    "flex items-center gap-3 text-left px-4 py-2 text-base font-medium transition-all duration-300",
                                    isOpen ? "w-full" : "w-full md:w-12 md:px-2 md:justify-center"
                                )}
                                onClick={() => setIsMobileOpen(false)}
                            >
                                <Icon className="h-5 w-5 flex-shrink-0" />
                                <span className={cn(isOpen ? "block" : "block md:hidden")}>{link.label}</span>
                            </Button>
                        );
                    })}
                </nav>

                <div className="mt-auto">
                    <button
                        className={cn(
                            "w-full flex items-center gap-2 px-4 py-2 text-base font-medium text-primary hover-halo rounded-md transition-all duration-300",
                            isOpen ? "" : "md:justify-center md:px-2"
                        )}
                        onClick={handleLogout}
                    >
                        <LogOut className="h-4 w-4" />
                        <span className={cn(isOpen ? "" : "md:hidden")}>Logout</span>
                    </button>
                </div>
            </aside>
        </>
    );
};

export default Sidebar;