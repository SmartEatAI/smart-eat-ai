import { ReactNode, useEffect } from "react";
import Sidebar from "./Sidebar";
interface PageHeaderProps {
  title: string;
  subtitle?: ReactNode;
  subtitleAlign?: 'right';
}

interface AppLayoutProps {
  title: string;
  subtitle?: ReactNode;
  subtitleAlign?: 'right';
  children: ReactNode;
}

export function AppLayout({title, subtitle, subtitleAlign, children}: AppLayoutProps) {
  useEffect(() => {
    document.body.classList.add("overflow-hidden");
    return () => {
      document.body.classList.remove("overflow-hidden");
    };
  }, []);


  return (
    <div className="flex min-h-screen h-screen">
      <Sidebar className="h-full"/>
      <div className="flex-1 h-full overflow-y-auto">
        <PageHeader title={title} subtitle={subtitle} subtitleAlign={subtitleAlign} />
        <main className="flex-1 p-6 pt-4 md:pt-6 lg:px-10">
          {children}
        </main>
      </div>
    </div>
  );
}

export function PageHeader({ title, subtitle, subtitleAlign }: PageHeaderProps) {
  if (subtitle && subtitleAlign === 'right') {
    return (
      <header className="sticky top-0 z-30 pb-6 bg-background border-b backdrop-blur-sm pl-14 pr-6 pt-6 md:px-10">
        <div className="flex items-center justify-between w-full">
          <h1 className="text-2xl font-bold tracking-tight text-primary">
            {title}
          </h1>
          <div className="ml-4 text-base md:text-lg text-muted-foreground">{subtitle}</div>
        </div>
      </header>
    );
  }
  return (
    <header className="sticky top-0 z-30 pb-6 bg-background border-b backdrop-blur-sm pl-14 pr-6 pt-6 md:px-10">
      <div className="space-y-1">
        <h1 className="text-2xl font-bold tracking-tight text-primary">
          {title}
        </h1>
        {subtitle && (
          <div className="text-muted-foreground text-sm">{subtitle}</div>
        )}
      </div>
    </header>
  );
}