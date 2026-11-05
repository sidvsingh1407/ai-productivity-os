import React from 'react';
import { ComingSoonLayout } from '../components/ComingSoonLayout';

const Terms: React.FC = () => {
  return (
    <ComingSoonLayout isShell={true}>
      <div className="py-8 text-cs-text-secondary font-sans prose prose-invert max-w-none">
        <h1 className="text-3xl md:text-4xl font-semibold mb-8 text-cs-text-primary">Terms of Service</h1>
        <p className="mb-4 font-medium">Last updated: [TO BE SET BY FOUNDER]</p>
        <p className="mb-4 text-base md:text-lg leading-relaxed">
          This is a placeholder. The real terms of service are under legal review and will be published before launch.
        </p>
        <p className="mb-4 text-base md:text-lg leading-relaxed">
          Tarkaya is not yet certified under ISO 27001. Certification is in progress. We will publish our certificate on this site once issued.
        </p>
        <p className="mt-8 text-base md:text-lg leading-relaxed">
          Contact: <a href="mailto:privacy@tarkaya.com" className="text-cs-accent hover:underline">privacy@tarkaya.com</a>
        </p>
      </div>
    </ComingSoonLayout>
  );
};

export default Terms;
