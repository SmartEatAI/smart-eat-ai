import React from "react";
import { ProfileProvider } from "@/context/ProfileContext";

export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  return (
    <ProfileProvider>
      {children}
    </ProfileProvider>
  );
}
