import React from 'react';
import { ComingSoonLayout } from '../components/ComingSoonLayout';

const DPA: React.FC = () => {
  return (
    <ComingSoonLayout isShell={true}>
      <div className="py-8 text-cs-text-secondary">
        <h1 className="text-3xl md:text-4xl font-semibold mb-8 text-cs-text-primary">Data Processing Agreement</h1>
        <h2 className="text-xl font-semibold mb-4 text-cs-text-primary">Legal Review Required</h2>
        <p className="mb-4 text-base md:text-lg leading-relaxed">
          This page does not represent a finalized, effective legal agreement.
        </p>
      </div>
    </ComingSoonLayout>
  );
};

export default DPA;
