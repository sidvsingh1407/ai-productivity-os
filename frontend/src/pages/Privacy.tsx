import React from 'react';
import { ComingSoonLayout } from '../components/ComingSoonLayout';

const Privacy: React.FC = () => {
  return (
    <ComingSoonLayout isShell={true}>
      <div className="py-8 text-cs-text-secondary font-sans prose prose-invert max-w-none">
        <h1 className="text-3xl md:text-4xl font-semibold mb-8 text-cs-text-primary">Privacy Policy</h1>
        <p className="mb-4 font-medium">Last updated: [TO BE SET BY FOUNDER]</p>
        <p className="mb-4 text-base md:text-lg leading-relaxed">
          This is a placeholder. The real privacy policy is under legal review and will be published before launch.
        </p>
        <p className="mb-4 text-base md:text-lg leading-relaxed">
          Tarkaya is pursuing ISO 27001 certification. We are not yet certified. For questions about our security posture, contact <a href="mailto:security@tarkaya.com" className="text-cs-accent hover:underline">security@tarkaya.com</a>.
        </p>
        <p className="mt-8 text-base md:text-lg leading-relaxed">
          Contact: <a href="mailto:privacy@tarkaya.com" className="text-cs-accent hover:underline">privacy@tarkaya.com</a>
        </p>
      </div>
    </ComingSoonLayout>
  );
};

export default Privacy;
