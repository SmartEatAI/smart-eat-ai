"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import Image from "next/image";
import { Eye } from "lucide-react";
import { FcGoogle } from "react-icons/fc";
import { FaApple } from "react-icons/fa";
import { useRouter } from "next/navigation";

import Button from "@/components/ui/Button";
import { loginSchema, registerSchema } from "@/schemas/auth.schema";

import "@/app/globals.css";

type AuthMode = "login" | "register";

const AuthForm: React.FC = () => {
    const [mode, setMode] = useState<AuthMode>("register");
    const [showPassword, setShowPassword] = useState(false);

    interface LoginFormData {
        email: string;
        password: string;
    }

    interface RegisterFormData extends LoginFormData {
        name: string;
    }

    type FormData = LoginFormData | RegisterFormData;

    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
    } = useForm<FormData>({
        resolver: zodResolver(mode === "login" ? loginSchema : registerSchema),
    });

    const router = useRouter();

    // LLAMADA SIMULADA A LA API
    const onSubmit = async (data: FormData) => {
        console.log(mode, data);

        try {
            const response: any = await new Promise((resolve, reject) => {
                setTimeout(() => {
                    if (data.email === "test@example.com" && data.password === "Password123") {
                        resolve({ success: true, message: "Login successful!" });
                    } else {
                        reject({ success: false, message: "Invalid credentials." });
                    }
                }, 1000);
            });

            if (response && response.message) {
                console.log("API Response:", response);
                alert(response.message);
                router.push("/"); // Redirigir al dashboard o página principal después del login/registro exitoso
            } else {
                throw new Error("Unexpected response format.");
            }
        } catch (error: any) {
            console.error("API Error:", error);
            alert(error?.message || "An unexpected error occurred.");
        }
    };

    return (
        <div className="flex min-h-screen">
            {/* Left Side - Form */}
            <div className="w-full lg:w-1/2 bg-[#0a1f1a] flex items-center justify-center p-8">
                <div className="w-full max-w-md space-y-8">
                    
                    {/* Logo */}
                    <div className="flex items-center gap-2 mb-6">
                        <div className="w-12 h-12 flex items-center justify-center text-4xl bg-green-400 rounded-full shadow-lg">
                            🥗
                        </div>
                        <div>
                            <span className="text-primary text-4xl font-extrabold">SmartEat </span>
                            <span className="text-green-300 text-4xl font-extrabold">AI</span>
                        </div>
                    </div>

                    {/* Title */}
                    <div className="space-y-2">
                        <h1 className="text-2xl font-semibold text-primary">
                            Start your journey
                        </h1>
                        <p className="text-gray-400 text-sm">
                            Create an account to unlock your personalized meal plan and nutritional tracking.
                        </p>
                    </div>

                    {/* Tabs */}
                    <div className="flex gap-8 border-b border-gray-700">
                        <button
                            type="button"
                            onClick={() => setMode("register")}
                            className={`pb-3 text-sm font-medium transition-colors relative ${
                                mode === "register" 
                                    ? "text-green-300" 
                                    : "text-primary hover-halo"
                            }`}
                        >
                            Sign Up
                            {mode === "register" && (
                                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-green-400" />
                            )}
                        </button>
                        <button
                            type="button"
                            onClick={() => setMode("login")}
                            className={`pb-3 text-sm font-medium transition-colors relative ${
                                mode === "login" 
                                    ? "text-green-400" 
                                    : "text-primary hover-halo"
                            }`}
                        >
                            Log In
                            {mode === "login" && (
                                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-green-400" />
                            )}
                        </button>
                    </div>

                    {/* Form */}
                    <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
                        
                        {mode === "register" && (
                            <div className="space-y-2">
                                <label className="text-sm text-gray-300">Full Name</label>
                                <input
                                    {...register("name")}
                                    placeholder="John Doe"
                                    className="w-full px-4 py-3 bg-transparent border border-gray-700 rounded-lg text-white placeholder:text-gray-500 focus:outline-none focus:border-green-400 transition-colors"
                                />
                                {errors && "name" in errors && (
                                    <p className="text-xs text-red-400">{(errors as any).name?.message}</p>
                                )}
                            </div>
                        )}

                        <div className="space-y-2">
                            <label className="text-sm text-gray-300">Email Address</label>
                            <input
                                {...register("email")}
                                type="email"
                                placeholder="you@example.com"
                                className="w-full px-4 py-3 bg-transparent border border-gray-700 rounded-lg text-white placeholder:text-gray-500 focus:outline-none focus:border-green-400 transition-colors"
                            />
                            {errors.email && (
                                <p className="text-xs text-red-400">{errors.email.message}</p>
                            )}
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm text-gray-300">Password</label>
                            <div className="relative">
                                <input
                                    {...register("password")}
                                    type={showPassword ? "text" : "password"}
                                    placeholder="Enter your password"
                                    className="w-full px-4 py-3 bg-transparent border border-gray-700 rounded-lg text-white placeholder:text-gray-500 focus:outline-none focus:border-green-400 transition-colors"
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-300"
                                >
                                    <Eye className="w-5 h-5" />
                                </button>
                            </div>
                            {errors.password && (
                                <p className="text-xs text-red-400">{errors.password.message}</p>
                            )}
                        </div>

                        <Button
                            type="submit"
                            disabled={isSubmitting}
                            variant="primary"
                            className="w-full py-3 flex items-center justify-center gap-2"
                        >
                            {mode === "register" ? "Continue to Onboarding" : "Log In"}
                            <span>→</span>
                        </Button>
                    </form>

                    {/* Social Login */}
                    <div className="space-y-4">
                        <div className="relative">
                            <div className="absolute inset-0 flex items-center">
                                <div className="w-full border-t border-gray-700" />
                            </div>
                            <div className="relative flex justify-center text-sm">
                                <span className="px-4 bg-[#0a1f1a] text-gray-400">
                                    Or continue with
                                </span>
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <button
                                type="button"
                                className="py-3 border border-gray-700 rounded-lg text-white hover:backdrop-blur-md hover:bg-white/10 transition-colors flex items-center justify-center gap-2"
                            >
                                <FcGoogle className="text-2xl" />
                                Google
                            </button>
                            <button
                                type="button"
                                className="py-3 border border-gray-700 rounded-lg text-white hover:backdrop-blur-md hover:bg-white/10 transition-colors flex items-center justify-center gap-2"
                            >
                                <FaApple className="text-2xl" />
                                Apple
                            </button>
                        </div>
                    </div>

                    {/* Terms */}
                    <p className="text-xs text-gray-500 text-center">
                        By continuing, you agree to SmartEatAI&apos;s{" "}
                        <a href="#" className="text-green-300 hover:underline">Terms of Service</a>
                        {" "}and{" "}
                        <a href="#" className="text-green-300 hover:underline">Privacy Policy</a>.
                    </p>
                </div>
            </div>

            {/* Right Side - Image & Testimonial */}
            <div className="hidden lg:flex lg:w-1/2 relative group">
                <Image
                    src="https://tse4.mm.bing.net/th/id/OIP.lEWsl3OXBrhkX2E2VFA00gHaJQ?w=1600&h=2000&rs=1&pid=ImgDetMain&o=7&rm=3"
                    alt="Healthy meal bowl"
                    fill
                    className="object-cover transition-transform duration-300 ease-in-out group-hover:brightness-75"
                />
            </div>
        </div>
    );
}

export default AuthForm;