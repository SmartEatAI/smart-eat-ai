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
      <div className="flex-1 p-6 pt-20 md:pt-6 h-full overflow-y-auto lg:p-10">
        <PageHeader title={title} subtitle={subtitle} />
        <main className="flex-1">
          {children}
        </main>
      </div>
    </div>
  );
}


export function PageHeader({ title, subtitle}: PageHeaderProps) {
  return (
    <header className="flex items-start justify-between gap-4 pb-6">
      <div className="space-y-1">
        <h1 className="text-3xl font-bold tracking-tight">
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
