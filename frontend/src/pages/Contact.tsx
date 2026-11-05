import React from 'react';
import { ComingSoonLayout } from '../components/ComingSoonLayout';

const Contact: React.FC = () => {
  return (
    <ComingSoonLayout>
      <section className="editorial-section editorial-section--light">
        <div className="editorial-container">
          <h1 className="editorial-heading">Contact</h1>
          <p className="editorial-body" style={{ marginBottom: '28px' }}>
            For general questions: <a href="mailto:privacy@tarkaya.com" style={{ color: '#000000', textDecoration: 'underline' }}>privacy@tarkaya.com</a>
          </p>
          <p className="editorial-body">
            For security or compliance questions: <a href="mailto:security@tarkaya.com" style={{ color: '#000000', textDecoration: 'underline' }}>security@tarkaya.com</a>
          </p>
        </div>
      </section>
    </ComingSoonLayout>
  );
};

export default Contact;
