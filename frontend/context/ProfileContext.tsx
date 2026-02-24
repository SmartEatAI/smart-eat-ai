"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { useAuth } from "@/hooks/useAuth";
import { User } from "@/types/user";

export interface Profile {
  id: number;
  user_id: number;
  goal: string;
  height: number;
  weight: number;
  body_type: string;
  gender: string;
  meals_per_day: number;
  activity_level: string;
  birth_date: string;
  body_fat_percentage?: number;
  calories_target?: number;
  protein_target?: number;
  carbs_target?: number;
  fat_target?: number;
  tastes?: any[];
  restrictions?: any[];
  diet_types?: any[];
}

interface ProfileContextType {
  profile: Profile | null;
  loading: boolean;
  error: string | null;
  fetchProfile: () => Promise<void>;
  updateProfile: (data: Partial<Profile>) => Promise<void>;
}

const ProfileContext = createContext<ProfileContextType | undefined>(undefined);

export const ProfileProvider = ({ children }: { children: ReactNode }) => {
  const { user } = useAuth();
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchProfile = async () => {
    if (!user) return;
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem("token");
      const res = await fetch("http://localhost:8000/api/profile/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!res.ok) throw new Error("No se pudo cargar el perfil");
      const data = await res.json();
      setProfile(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const updateProfile = async (data: Partial<Profile>) => {
    if (!user) return;
    setLoading(true);
    setError(null);
    try {
      // Normalizar diet_types, tastes y restrictions a arrays de strings
      // tastes y restrictions deben ser [{ name: string }], diet_types: [string]
      const normalizeNames = (arr: any) => Array.isArray(arr)
        ? arr.map((item) => typeof item === "string" ? { name: item } : { name: item.name })
        : [];
      const normalizeStrings = (arr: any) => Array.isArray(arr)
        ? arr.map((item) => typeof item === "string" ? item : item.name)
        : [];
      const payload = {
        ...data,
        diet_types: normalizeStrings(data.diet_types),
        tastes: normalizeNames(data.tastes),
        restrictions: normalizeNames(data.restrictions),
      };
      
      /*#######################################
        DEBUG: Ver el payload antes de enviarlo
        #######################################*/
      console.log("Updating profile with data:", payload);
      
      const token = localStorage.getItem("token");
      const res = await fetch("http://localhost:8000/api/profile/", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error("No se pudo actualizar el perfil");
      const updated = await res.json();
      setProfile(updated);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user) fetchProfile();
    else setProfile(null);
    // eslint-disable-next-line
  }, [user]);

  return (
    <ProfileContext.Provider value={{ profile, loading, error, fetchProfile, updateProfile }}>
      {children}
    </ProfileContext.Provider>
  );
};

export const useProfileContext = () => {
  const ctx = useContext(ProfileContext);
  if (!ctx) throw new Error("useProfileContext debe usarse dentro de ProfileProvider");
  return ctx;
};
