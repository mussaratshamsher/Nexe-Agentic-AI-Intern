import React from 'react';
import { cn } from '@/lib/utils';

interface CommandCenterCardProps {
  children: React.ReactNode;
  className?: string;
  glow?: 'blue' | 'purple' | 'white' | 'green' |'none';
}

export const CommandCenterCard = ({
  children,
  className,
  glow = 'none',
}: CommandCenterCardProps) => {
  return (
    <div
      className={cn(
        'glass rounded-2xl p-6 transition-all duration-300 hover:border-white/20',
        glow === 'blue' && 'glow-blue hover:border-primary/50',
        glow === 'purple' && 'glow-purple hover:border-accent/50',
        glow === 'white' && 'glow-white hover:border-white/50',
        glow === 'green' && 'glow-green hover:border-emerald-400/50',
        glow === 'none' && 'hover:border-transparent',
        className
      )}
    >
      {children}
    </div>
  );
};
