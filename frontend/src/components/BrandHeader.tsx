import React from 'react';

export const BrandHeader: React.FC = () => {
  return (
    <div className="fixed top-0 left-0 right-0 z-50 flex justify-center pt-4 md:pt-8 pointer-events-none">
      <span className="text-sm md:text-base font-semibold tracking-[0.2em] text-cs-text-primary pointer-events-auto select-none uppercase">
        TARKAYA
      </span>
    </div>
  );
};
