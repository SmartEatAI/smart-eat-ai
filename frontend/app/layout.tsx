import type { Metadata } from "next";
import { Figtree } from 'next/font/google';

import "./globals.css";
import { AuthProvider } from "../context/AuthContext";
import { ProfileProvider } from "../context/ProfileContext";

const figtree = Figtree({
  variable: '--font-figtree',
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700', '800', '900'],
  style: ['normal', 'italic'],
});



export const metadata: Metadata = {
  title: "SmartEat AI",
  description: "Personalized nutrition and meal planning powered by AI.",
  icons: {
    icon: "/images/salad-icon.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className="dark">
      <body className={`${figtree.variable} antialiased`}>
        <AuthProvider>
          <ProfileProvider>
            {children}
          </ProfileProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
