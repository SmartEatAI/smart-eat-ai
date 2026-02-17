type ButtonVariant = "primary" | "secondary" | "day";

interface ButtonProps {
    as?: React.ElementType;
    children: React.ReactNode;
    variant?: ButtonVariant;
    className?: string;
    [key: string]: any;
}

const Button: React.FC<ButtonProps> = ({
    as: Component = "button",
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
        day: "bg-surface-dark text-[#9db9ab] hover:bg-[#283930] hover:text-primary hover:shadow-[0_0_10px_2px_rgba(72,187,120,0.8)]",
    };

    return (
        <Component className={`${baseStyles} ${variants[variant]} ${className}`} {...props}>
            {children}
        </Component>
    );
};

export default Button;