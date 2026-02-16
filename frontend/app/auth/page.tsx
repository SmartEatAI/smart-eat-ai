import AuthForm from "@/components/auth/AuthForm";
import PublicRoute from "@/components/auth/PublicRoute";

export default function AuthPage() {
    return (
        <PublicRoute>
            <AuthForm />
        </PublicRoute>
    );
}
