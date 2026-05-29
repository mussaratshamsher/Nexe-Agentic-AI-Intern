import React from 'react';

interface ProjectCardProps {
  title: string;
  techStack: string;
  features: string[];
  href: string;
}

export const ProjectCard: React.FC<ProjectCardProps> = ({ title, techStack, features, href }) => {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="block p-4 rounded-xl border border-border/50 bg-card hover:bg-accent/10 hover:border-primary/50 transition-all duration-200 group shadow-sm"
    >
      <h4 className="text-sm font-semibold text-foreground group-hover:text-primary transition-colors">
        {title}
      </h4>
      <p className="text-xs text-muted-foreground mt-1 font-mono uppercase tracking-wider">
        {techStack}
      </p>
      <ul className="mt-3 space-y-1">
        {features.map((feature, index) => (
          <li key={index} className="text-xs text-muted-foreground flex items-center gap-2">
            <span className="w-1 h-1 rounded-full bg-primary/40" />
            {feature}
          </li>
        ))}
      </ul>
    </a>
  );
};
