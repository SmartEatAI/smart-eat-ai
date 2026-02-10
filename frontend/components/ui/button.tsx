import React from "react";

type ButtonVariant = "primary" | "secondary";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    children: React.ReactNode;
    variant?: ButtonVariant;
}

const Button: React.FC<ButtonProps> = ({
    children,
    variant = "primary",
    className = "",
    ...props
}) => {
    const baseStyles = "px-4 py-2 rounded-md transition-all duration-300";
    const variants: Record<ButtonVariant, string> = {
        primary:
        "bg-green-500 text-primary hover:bg-green-400 hover:shadow-[0_0_10px_2px_rgba(72,187,120,0.8)]",
        secondary:
        "text-primary hover:bg-green-400 hover:text-primary hover:shadow-[0_0_10px_2px_rgba(72,187,120,0.8)]",
    };

    return (
        <button className={`${baseStyles} ${variants[variant]} ${className}`} {...props}>
            {children}
        </button>
    );
};

export default Button;