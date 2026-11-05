import React from 'react';
import { ComingSoonLayout } from '../components/ComingSoonLayout';

const Terms: React.FC = () => {
  return (
    <ComingSoonLayout>
      <section className="editorial-section editorial-section--light">
        <div className="editorial-container">
          <h1 className="editorial-heading">Terms of Service</h1>
          <p className="editorial-body" style={{ marginBottom: '28px' }}>Last updated: [TO BE SET BY FOUNDER]</p>
          <p className="editorial-body" style={{ marginBottom: '28px' }}>
            This is a placeholder. The real terms of service are under legal review and will be published before launch.
          </p>
          <p className="editorial-body">
            Contact: <a href="mailto:privacy@tarkaya.com" style={{ color: '#000000', textDecoration: 'underline' }}>privacy@tarkaya.com</a>
          </p>
        </div>
      </section>
    </ComingSoonLayout>
  );
};

export default Terms;
