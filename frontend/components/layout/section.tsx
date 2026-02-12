interface SectionProps {
  id?: string;
  title?: string;
  subtitle?: string;
  className?: string;
  children: React.ReactNode;
}

const Section: React.FC<SectionProps> = ({
  id,
  title,
  subtitle,
  className = "",
  children,
}) => {
  return (
    <section
      id={id}
      className={`w-full flex justify-center ${className}`}
    >
      <div className="w-full max-w-7xl px-6 md:px-8 py-10">
        {(title || subtitle) && (
          <header className="mb-10 text-center">
            {title && (
              <h2 className="text-3xl font-bold">
                {title}
              </h2>
            )}
            {subtitle && (
              <p className="mt-2 text-muted-foreground">
                {subtitle}
              </p>
            )}
          </header>
        )}

        {children}
      </div>
    </section>
  );
};

export default Section;
