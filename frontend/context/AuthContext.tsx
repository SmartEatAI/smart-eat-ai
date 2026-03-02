"use client"

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User } from '../types/user';
import { useRouter } from "next/navigation";

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (userData: User, token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState<string | null>(null);
  const [isValid, setIsValid] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Aquí puedes cargar el usuario desde localStorage o cookies si es necesario
    const storedUser = localStorage.getItem('user');
    const storedToken = localStorage.getItem('token');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }

    if (storedToken) {
      setToken(storedToken);
    }
    
    setLoading(false);
  }, []);

  useEffect(() => {
    if (!token) return;

    const intervalId = setInterval(async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/auth/?token=${token}`);
        const valid = await response.json(); // true o false
        setIsValid(valid);

        if (!valid) {
          console.log("Token inválido, limpiando sesión...");
          clearInterval(intervalId);
          logout(); // Limpiar usuario y token
          router.push("/auth"); // Redirigir a login
        }
      } catch (error) {
        console.error("Error verificando token:", error);
        setIsValid(false);
        clearInterval(intervalId);
      }
    }, 60000); // Cada minuto

    return () => clearInterval(intervalId); // Limpieza al desmontar
  }, [token]);

  const login = (userData: User, token: string) => {
    setUser(userData);
    setToken(token);
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('token', token);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuthContext = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuthContext debe usarse dentro de un AuthProvider');
  }
  return context;
};
