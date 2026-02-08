import React from "react";

type ButtonVariant = "primary" | "secondary";

interface ButtonProps {
    children: React.ReactNode;
    variant?: ButtonVariant;
    onClick?: () => void;
}

const Button: React.FC<ButtonProps> = ({
    children,
    variant = "primary",
    onClick,
}) => {
    const baseStyles = "px-4 py-2 rounded-md transition-all duration-300";
    const variants: Record<ButtonVariant, string> = {
        primary:
        "bg-green-500 text-white hover:bg-green-400 hover:shadow-[0_0_10px_2px_rgba(72,187,120,0.8)]",
        secondary:
        "text-gray-200 hover:bg-green-400 hover:text-white hover:shadow-[0_0_10px_2px_rgba(72,187,120,0.8)]",
    };

    return (
        <button className={`${baseStyles} ${variants[variant]}`} onClick={onClick}>
            {children}
        </button>
    );
};

export default Button;