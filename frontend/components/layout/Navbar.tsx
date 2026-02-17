"use client";

import Button from "@/components/ui/Button";

const Navbar: React.FC = () => {
    return (
    <nav className="bg-green-950/70 backdrop-blur-md shadow-sm sticky top-0 z-50">
        <div className="container mx-auto py-5 flex items-center justify-between">
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

            {/* Navigation Links */}
            <div className="flex items-center gap-6 mx-auto">
                <a href="#inicio" className="text-primary hover-halo">Home</a>
                <a href="#why-smarteat" className="text-primary hover-halo">Why Choose Us</a>
                <a href="#how-it-works" className="text-primary hover-halo">How It Works</a>
                <a href="#plans" className="text-primary hover-halo">Plans</a>
                <a href="#reviews" className="text-primary hover-halo">Testimonials</a>
                <a href="#cta" className="text-primary hover-halo">Contact</a>
            </div>

            {/* Buttons */}
            <div className="flex gap-3">
                <Button variant="secondary" as="a" href="/auth">Log in</Button>
                <Button variant="primary" as="a" href="/auth">Sign up</Button>
            </div>
        </div>
    </nav>
    );
};

export default Navbar;