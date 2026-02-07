"use client";

import Button from "@/components/ui/Button";

const Navbar: React.FC = () => {
    return (
    <nav className="bg-green-950 shadow-sm">
        <div className="container mx-auto px-8 py-5 flex items-center justify-between">
        {/* Logo */}
        <div
            className="text-2xl font-bold text-green-400 hover:text-green-300 transition-all duration-300 cursor-pointer"
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

        {/* Buttons */}
        <div className="flex gap-3">
            <Button variant="secondary">Log in</Button>
            <Button variant="primary">Sign up</Button>
        </div>
        </div>
    </nav>
    );
};

export default Navbar;
