"use client";

import { useEffect } from "react";
import { X, CheckCircle, AlertCircle } from "lucide-react";

interface ToastProps {
    message: string;
    type?: "success" | "error";
    onClose: () => void;
    duration?: number;
}

const Toast: React.FC<ToastProps> = ({ message, type = "success", onClose, duration = 3000 }) => {
    useEffect(() => {
        const timer = setTimeout(() => {
            onClose();
        }, duration);

        return () => clearTimeout(timer);
    }, [duration, onClose]);

    return (
        <div
            className={`fixed top-4 right-4 z-100 flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg backdrop-blur-md animate-in slide-in-from-top-5 ${
                type === "success"
                    ? "bg-green-500/90 text-white"
                    : "bg-red-500/90 text-white"
            }`} style={{ marginRight: 8 }}
        >
            {type === "success" ? (
                <CheckCircle className="h-5 w-5 shrink-0" />
            ) : (
                <AlertCircle className="h-5 w-5 shrink-0" />
            )}
            <p className="text-sm font-medium">{message}</p>
            <button
                onClick={onClose}
                className="ml-2 hover:bg-white/20 rounded-full p-1 transition-colors"
            >
                <X className="h-4 w-4" />
            </button>
        </div>
    );
};

export default Toast;
