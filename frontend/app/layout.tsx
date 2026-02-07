import "./globals.css";
import Navbar from "@/components/layout/header/Navbar";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-green-950">
        <Navbar />
        {children}
      </body>
    </html>
  );
}
