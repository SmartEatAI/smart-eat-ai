/**
 * User types matching backend UserResponse schema
 * Backend fields are in Spanish (nombre, correo)
 */

export interface User {
    id: number;
    nombre: string;
    correo: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
    user: User;
}
