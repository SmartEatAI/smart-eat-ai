import { Twitter, Instagram, Linkedin } from "lucide-react";

const Footer: React.FC = () => {
    return (
        <footer className="bg-green-950 border-t border-green-900/40">
            <div className="container mx-auto px-4 py-12 flex flex-col gap-10">
                
                {/* Top */}
                <div className="flex flex-col md:flex-row justify-between gap-10">
                
                    {/* Brand */}
                    <div>
                        <h2 
                            className="text-2xl font-bold text-primary mb-3 hover:text-green-300 transition-all duration-300 cursor-pointer"
                            onMouseEnter={(e) => {
                                e.currentTarget.style.textShadow =
                                "0 0 10px rgba(72,187,120,0.8), 0 0 20px rgba(72,187,120,0.6)";
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.textShadow = "none";
                            }}
                        >
                            🥗 SmartEatAI
                        </h2>
                        <p className="text-sm text-primary/70 max-w-sm">
                            AI-powered nutrition plans designed to help you eat smarter,
                            live healthier, and feel better every day.
                        </p>
                    </div>

                    {/* Links */}
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-8 text-sm">
                        <div className="flex flex-col gap-3">
                            <span className="text-green-300 font-semibold">Product</span>
                            <a href="#inicio" className="text-primary hover-halo">Home</a>
                            <a href="#how-it-works" className="text-primary hover-halo">How It Works</a>
                            <a href="#plans" className="text-primary hover-halo">Plans</a>
                        </div>

                        <div className="flex flex-col gap-3">
                            <span className="text-green-300 font-semibold">Why SmartEat</span>
                            <a href="#why-smarteat" className="text-primary hover-halo">Why Choose Us</a>
                            <a href="#reviews" className="text-primary hover-halo">Testimonials</a>
                        </div>

                        <div className="flex flex-col gap-3">
                            <span className="text-green-300 font-semibold">Contact</span>
                            <a href="#cta" className="text-primary hover-halo">Get in Touch</a>
                            <a href="/privacy" className="text-primary hover-halo">Privacy Policy</a>
                            <a href="/terms" className="text-primary hover-halo">Terms of Service</a>
                        </div>
                    </div>
                </div>

                {/* Bottom */}
                <div className="border-t border-green-900/40 pt-6 flex flex-col sm:flex-row items-center justify-between gap-4">
                    <p className="text-xs text-primary/70">
                        © {new Date().getFullYear()} SmartEatAI. All rights reserved.
                    </p>

                    <div className="flex gap-8 pe-3">
                        <a href="#" className="text-primary hover-halo" aria-label="Twitter">
                            <Twitter className="w-5 h-5" />
                        </a>
                        <a href="#" className="text-primary hover-halo" aria-label="Instagram">
                            <Instagram className="w-5 h-5" />
                        </a>
                        <a href="#" className="text-primary hover-halo" aria-label="LinkedIn">
                            <Linkedin className="w-5 h-5" />
                        </a>
                    </div>
                </div>
            </div>
        </footer>
    );
}

export default Footer;
