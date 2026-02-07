import Image from "next/image";
import Button from "@/components/ui/Button";

const Hero: React.FC = () => {
    return (
        <section className="w-full bg-green-900 pt-16 pb-16">
            <div className="container mx-auto px-8 flex flex-col md:flex-row items-center justify-between">
                {/* Left text */}
                <div className="md:w-1/2">
                <h1 className="text-3xl md:text-4xl font-bold text-gray-200 mb-4">
                    Eat smarter,
                </h1>
                <h1 className="text-4xl md:text-5xl font-bold text-green-400 mb-4">
                    SmartEatAI
                </h1>
                <p className="text-gray-200 mb-6">
                    Personalize your diet with AI, learn about macros, and discover recipes optimized for your goals.
                </p>
                <Button variant="primary">
                    Get Started
                </Button>
                </div>

                {/* Right image */}
                <div className="md:w-1/2 mt-10 md:mt-0 flex justify-end">
                <div className="w-full max-w-lg p-4">
                    <Image
                    src="/img/hero-img.jpg"
                    alt="Hero"
                    width={800}
                    height={500}
                    className="rounded-lg shadow-2xl shadow-green-700 transition-transform hover:scale-105 hover:brightness-75 object-cover max-h-100"
                    />
                </div>
                </div>
            </div>
        </section>
    );
};

export default Hero;
