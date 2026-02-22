/**
 * User types matching backend UserResponse schema
 * All fields are in English
 */

export interface User {
    id: number;
    name: string;
    email: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
    user: User;
}
