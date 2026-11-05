import React from 'react';
import { ComingSoonLayout } from '../components/ComingSoonLayout';

const Contact: React.FC = () => {
  return (
    <ComingSoonLayout isShell={true}>
      <div className="py-8 text-cs-text-secondary font-sans prose prose-invert max-w-none text-left">
        <h1 className="text-3xl md:text-4xl font-semibold mb-6 text-cs-text-primary">Contact</h1>
        <p className="mb-4 text-base md:text-lg leading-relaxed">
          For general questions: <a href="mailto:privacy@tarkaya.com" className="text-cs-accent hover:underline">privacy@tarkaya.com</a>
        </p>
        <p className="mb-4 text-base md:text-lg leading-relaxed">
          For security or compliance questions: <a href="mailto:security@tarkaya.com" className="text-cs-accent hover:underline">security@tarkaya.com</a>
        </p>
        <p className="mt-8 text-base md:text-lg leading-relaxed text-cs-text-muted">
          Tarkaya is not yet ISO 27001 certified. Certification is in progress.
        </p>
      </div>
    </ComingSoonLayout>
  );
};

export default Contact;
