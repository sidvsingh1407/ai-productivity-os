import React from 'react';
import { ComingSoonLayout } from '../components/ComingSoonLayout';

const Terms: React.FC = () => {
  return (
    <ComingSoonLayout isShell={true}>
      <div className="py-8 text-cs-text-secondary">
        <h1 className="text-3xl md:text-4xl font-semibold mb-8 text-cs-text-primary">Terms of Service</h1>
        <p className="mb-4">Last updated: [Date]</p>
        <p className="mb-4 text-base md:text-lg leading-relaxed">
          These Terms of Service govern your access to and use of Tarkaya's website and services.
        </p>
        {/* Placeholder for actual terms content */}
        <div className="h-64 bg-[rgba(255,255,255,0.02)] rounded-lg border border-glass-border flex items-center justify-center">
          <p className="text-cs-text-muted italic">Legal content requires formal review.</p>
        </div>
      </div>
    </ComingSoonLayout>
  );
};

export default Terms;
