export interface ToastState {
    message: string;
    type: "success" | "error";
}

export interface LoginFormData {
        email: string;
        password: string;
    }

export interface RegisterFormData extends LoginFormData {
        name: string;
    }

export type FormData = LoginFormData | RegisterFormData;

export type AuthMode = "login" | "register";