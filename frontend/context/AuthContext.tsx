"use client"

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import Toast from "@/components/ui/Toast";
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
  const [showTokenExpired, setShowTokenExpired] = useState(false);

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

    // Listener para detectar cambios en localStorage (incluyendo borrado manual)
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'token' && !e.newValue && token) {
        // Token fue eliminado manualmente
        console.log("Token eliminado del localStorage");
        setShowTokenExpired(true);
        setUser(null);
        setToken(null);
        setTimeout(() => {
          setShowTokenExpired(false);
          router.push("/auth?mode=login");
        }, 2000);
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [token, router]);

  useEffect(() => {
    if (!token) return;

    const checkToken = async () => {
      // Primero verificar si el token sigue en localStorage
      const storedToken = localStorage.getItem('token');
      if (!storedToken) {
        console.log("Token eliminado del localStorage");
        setShowTokenExpired(true);
        setUser(null);
        setToken(null);
        setTimeout(() => {
          setShowTokenExpired(false);
          router.push("/auth?mode=login");
        }, 2000);
        return;
      }

      try {
        const response = await fetch(`http://localhost:8000/api/auth/?token=${token}`);
        const valid = await response.json(); // true o false
        setIsValid(valid);

        if (!valid) {
          console.log("Token inválido, limpiando sesión...");
          setShowTokenExpired(true);
          logout(); // Limpiar usuario y token
          setTimeout(() => {
            setShowTokenExpired(false);
            router.push("/auth?mode=login");
          }, 2000);
        }
      } catch (error) {
        console.error("Error verificando token:", error);
        setIsValid(false);
        setShowTokenExpired(true);
        logout();
        setTimeout(() => {
          setShowTokenExpired(false);
          router.push("/auth?mode=login");
        }, 2000);
      }
    };

    // Chequeo inmediato al montar
    checkToken();
    // Chequeo cada 10 segundos (más frecuente para detectar cambios manuales)
    const intervalId = setInterval(checkToken, 10000);
    return () => clearInterval(intervalId);
  }, [token, router]);

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
      {showTokenExpired && (
        <Toast
          message="Your session has expired. Please log in again."
          type="error"
          onClose={() => setShowTokenExpired(false)}
        />
      )}
    </AuthContext.Provider>
  );
};

export const useAuthContext = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }
  return context;
};
