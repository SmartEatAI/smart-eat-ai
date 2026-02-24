"use client";

import Button from "@/components/ui/Button";
import { useState } from "react";
import { Menu, X } from "lucide-react";
import { cn } from "@/lib/utils";

const navLinks = [
    { href: "#inicio", label: "Home" },
    { href: "#why-smarteat", label: "Why Choose Us" },
    { href: "#how-it-works", label: "How It Works" },
    { href: "#plans", label: "Plans" },
    { href: "#reviews", label: "Testimonials" },
    { href: "#cta", label: "Contact" },
];

const Navbar: React.FC = () => {
    const [mobileOpen, setMobileOpen] = useState(false);

    return (
        <nav className="bg-green-950/70 backdrop-blur-md shadow-sm sticky top-0 z-50">
            <div className="container mx-auto py-5 flex items-center justify-between px-4 md:px-0">
                {/* Logo */}
                <div
                    className="text-2xl font-bold text-primary hover:text-green-300 transition-all duration-300 cursor-pointer"
                    onMouseEnter={(e) => {
                        e.currentTarget.style.textShadow =
                            "0 0 10px rgba(72,187,120,0.8), 0 0 20px rgba(72,187,120,0.6)";
                    }}
                    onMouseLeave={(e) => {
                        e.currentTarget.style.textShadow = "none";
                    }}
                >
                    🥗 SmartEatAI
                </div>

                {/* Desktop Nav */}
                <div className="hidden md:flex items-center gap-6 mx-auto">
                    {navLinks.map((link) => (
                        <a key={link.href} href={link.href} className="text-primary hover-halo">
                            {link.label}
                        </a>
                    ))}
                </div>

                {/* Desktop Buttons */}
                <div className="hidden md:flex gap-3">
                    <Button variant="secondary" as="a" href="/auth">Log in</Button>
                    <Button variant="primary" as="a" href="/auth">Sign up</Button>
                </div>

                {/* Mobile Menu Button */}
                <button
                    className="md:hidden p-2.5 bg-green-950/70 text-primary rounded-full shadow-lg hover:bg-secondary transition-all duration-300"
                    onClick={() => setMobileOpen(true)}
                    aria-label="Open menu"
                >
                    <Menu className="h-5 w-5" />
                </button>
            </div>

            {/* Mobile Overlay */}
            {mobileOpen && (
                <div
                    className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
                    onClick={() => setMobileOpen(false)}
                />
            )}

            {/* Mobile Dropdown Menu */}
            <div
                className={cn(
                    "fixed left-0 top-0 w-full z-50 md:hidden transition-all duration-300",
                    mobileOpen ? "max-h-screen opacity-100" : "max-h-0 opacity-0 pointer-events-none",
                )}
                style={{
                    overflow: "hidden",
                    background: "rgba(20, 83, 45, 0.95)",
                    backdropFilter: "blur(8px)",
                }}
            >
                <div className="flex items-center justify-between px-6 py-5 border-b border-green-800">
                    <span
                        className="font-bold text-primary text-xl cursor-pointer"
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
                    <button
                        className="p-2.5 bg-green-950/70 text-primary rounded-full shadow-lg hover:bg-secondary transition-all duration-300"
                        onClick={() => setMobileOpen(false)}
                        aria-label="Close menu"
                    >
                        <X className="h-5 w-5" />
                    </button>
                </div>
                <nav className="flex flex-col gap-6 px-6 py-6">
                    {navLinks.map((link) => (
                        <a
                            key={link.href}
                            href={link.href}
                            className="text-primary text-lg hover-halo"
                            onClick={() => setMobileOpen(false)}
                        >
                            {link.label}
                        </a>
                    ))}
                </nav>
                <div className="flex flex-col gap-3 px-6 pb-6 justify-center w-full">
                    <Button     
                        variant="secondary"
                        as="a" 
                        href="/auth" 
                        onClick={() => setMobileOpen(false)}
                        className="flex-1"
                    >
                        Log in
                    </Button>
                    <Button 
                        variant="primary" 
                        as="a" href="/auth" 
                        onClick={() => setMobileOpen(false)} className="flex-1"
                    >
                        Sign up
                    </Button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;