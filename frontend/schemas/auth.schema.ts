import { z } from "zod";

export const loginSchema = z.object({
    email: z
        .email("Please enter a valid email address"),
    password: z
        .string()
        .min(8, "Password must be at least 8 characters long")
        .regex(/[A-Z]/, "Password must include at least one uppercase letter")
        .regex(/[a-z]/, "Password must include at least one lowercase letter")
        .regex(/[0-9]/, "Password must include at least one number")
        //.regex(/[^A-Za-z0-9]/, "Password must include at least one special character"),
});

export const registerSchema = loginSchema.extend({
    name: z
        .string()
        .trim()
        .min(2, "Name must be at least 2 characters long")
        .max(50, "Name must be less than 50 characters long")
        .regex(/^[a-zA-Z ]+$/, "Name can only contain letters and spaces"),
});