import { ReactNode } from "react";
import Sidebar from "./Sidebar";

interface PageHeaderProps {
  title: string;
  subtitle?: string;
}

interface AppLayoutProps {
  title: string;
  subtitle?: string;
  children: ReactNode;
}

export function AppLayout({title, subtitle, children}: AppLayoutProps) {
  return (
    <div className="flex min-h-screen h-screen">
      <Sidebar className="h-full"/>
      <div className="flex-1 h-full overflow-y-auto">
        <PageHeader title={title} subtitle={subtitle} />
        <main className="flex-1 p-6 pt-4 md:pt-6 lg:px-10">
          {children}
        </main>
      </div>
    </div>
  );
}

export function PageHeader({ title, subtitle}: PageHeaderProps) {
  return (
    <header className="sticky top-0 z-30 flex items-start justify-between gap-4 pb-6 bg-background border-b backdrop-blur-sm px-6 pt-6 md:px-10">
      <div className="space-y-1">
        <h1 className="text-2xl font-bold tracking-tight text-primary">
          {title}
        </h1>
        {subtitle && (
          <p className="text-muted-foreground text-sm">
            {subtitle}
          </p>
        )}
      </div>
    </header>
  );
}