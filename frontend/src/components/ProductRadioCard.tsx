import React, { useRef } from 'react';
import { GlassPanel } from './GlassPanel';
import { cn } from '../lib/utils';

export type ProductRadioCardProps = {
  id: 'readiness' | 'workflow' | 'roadmap' | 'prompt' | 'strategy' | 'unsure';
  title: string;
  description: string;
  selected: boolean;
  onSelect: (id: string) => void;
  onDeselect: () => void;
};

export const ProductRadioCard: React.FC<ProductRadioCardProps> = ({
  id,
  title,
  description,
  selected,
  onSelect,
  onDeselect,
}) => {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleClick = () => {
    if (selected) {
      onDeselect();
    } else {
      onSelect(id);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  };

  return (
    <GlassPanel
      role="button"
      tabIndex={0}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      aria-checked={selected}
      className={cn(
        "p-4 cursor-pointer relative transition-all duration-200 text-left min-h-[120px] flex flex-col justify-center outline-none",
        selected
          ? "border-cs-accent shadow-[0_0_20px_rgba(94,234,212,0.15)] bg-glass-hover border-[2px]"
          : "border-glass-border focus-visible:ring-2 focus-visible:ring-cs-accent focus-visible:ring-offset-2 focus-visible:ring-offset-cs-bg-base hover:border-[rgba(255,255,255,0.2)]"
      )}
    >
      <input
        type="radio"
        id={`product-${id}`}
        name="product_preference"
        value={title}
        checked={selected}
        onChange={() => {}} // Controlled via parent
        className="sr-only"
        aria-labelledby={`product-${id}-title`}
        ref={inputRef}
      />
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <span id={`product-${id}-title`} className={cn("font-medium", selected ? "text-cs-text-primary" : "text-cs-text-secondary")}>
            {title}
          </span>
          {/* Custom radio button visualization */}
          <div className={cn(
            "w-4 h-4 rounded-full border flex items-center justify-center transition-colors",
            selected ? "border-cs-accent" : "border-cs-text-muted"
          )}>
            {selected && <div className="w-2 h-2 rounded-full bg-cs-accent" />}
          </div>
        </div>
        <p className="text-sm text-cs-text-secondary leading-relaxed">
          {description}
        </p>
      </div>
    </GlassPanel>
  );
};
