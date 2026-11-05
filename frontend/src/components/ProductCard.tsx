import React from 'react';
import { GlassPanel } from './GlassPanel';

interface ProductCardProps {
  name: string;
  copy: string;
}

export const ProductCard: React.FC<ProductCardProps> = ({ name, copy }) => {
  return (
    <GlassPanel className="p-6 min-h-[180px] h-full flex flex-col hover:-translate-y-[2px] transition-transform duration-200 group">
      <div className="absolute top-0 left-0 w-full h-[1px] bg-transparent group-hover:bg-cs-accent transition-colors duration-200 rounded-t-[1rem]"></div>
      <h3 className="text-xl font-medium mb-3 text-cs-text-primary">{name}</h3>
      <p className="text-base md:text-lg text-cs-text-secondary leading-relaxed flex-grow">{copy}</p>
    </GlassPanel>
  );
};
