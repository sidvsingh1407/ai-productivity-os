import React from 'react';
import { cn } from '../lib/utils';

interface GlassPanelProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export const GlassPanel: React.FC<GlassPanelProps> = ({ children, className, ...props }) => {
  return (
    <div
      className={cn(
        "glass-panel text-cs-text-primary transition-all duration-200 hover:bg-glass-hover hover:border-[rgba(255,255,255,0.2)] md:backdrop-blur-glass backdrop-blur-[12px]",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};
