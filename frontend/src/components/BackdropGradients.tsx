import React from 'react';

export const BackdropGradients: React.FC = () => {
  return (
    <>
      <div
        className="fixed top-0 left-0 w-[800px] h-[800px] bg-cs-bg-gradient-1 rounded-full blur-[120px] opacity-60 pointer-events-none -translate-x-1/4 -translate-y-1/4"
        style={{ willChange: 'auto' }}
      />
      <div
        className="fixed bottom-0 right-0 w-[600px] h-[600px] bg-cs-bg-gradient-2 rounded-full blur-[120px] opacity-50 pointer-events-none translate-x-1/4 translate-y-1/4"
        style={{ willChange: 'auto' }}
      />
    </>
  );
};
