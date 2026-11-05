import React from 'react';
import { ComingSoonLayout } from '../components/ComingSoonLayout';

const Contact: React.FC = () => {
  return (
    <ComingSoonLayout isShell={true}>
      <div className="py-8 text-cs-text-secondary text-center">
        <h1 className="text-3xl md:text-4xl font-semibold mb-6 text-cs-text-primary">Contact Us</h1>
        <p className="mb-8 text-base md:text-lg leading-relaxed">
          Have questions? We'd love to hear from you.
        </p>
        <a
          href="mailto:contact@tarkaya.com"
          className="inline-block px-6 py-3 bg-[rgba(255,255,255,0.04)] border border-glass-border rounded-lg text-cs-text-primary hover:bg-glass-hover focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base transition-colors"
        >
          contact@tarkaya.com
        </a>
      </div>
    </ComingSoonLayout>
  );
};

export default Contact;
