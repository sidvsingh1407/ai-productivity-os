import React from 'react';
import { Link } from 'react-router-dom';
import { ComingSoonLayout } from '../components/ComingSoonLayout';

const Expired: React.FC = () => {
  return (
    <ComingSoonLayout isShell={true}>
      <div className="text-center py-12">
        <h1 className="text-3xl md:text-4xl font-semibold mb-4 text-cs-text-primary">Link expired</h1>
        <p className="text-base md:text-lg text-cs-text-secondary mb-8">
          This confirmation link has expired or has already been used.
        </p>
        <Link
          to="/"
          className="inline-block px-6 py-3 bg-[rgba(255,255,255,0.04)] border border-glass-border rounded-lg text-cs-text-primary hover:bg-glass-hover focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base transition-colors"
        >
          Return home
        </Link>
      </div>
    </ComingSoonLayout>
  );
};

export default Expired;
