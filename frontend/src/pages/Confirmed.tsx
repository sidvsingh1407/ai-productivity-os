import React from 'react';
import { Link } from 'react-router-dom';
import { ComingSoonLayout } from '../components/ComingSoonLayout';

const Confirmed: React.FC = () => {
  return (
    <ComingSoonLayout>
      <section className="editorial-section editorial-section--light">
        <div className="editorial-container" style={{ textAlign: 'center' }}>
          <h1 className="editorial-heading">You're on the list</h1>
          <p className="editorial-body" style={{ margin: '0 auto 40px auto' }}>
            Thank you for confirming your email address. We'll be in touch soon.
          </p>
          <Link to="/" className="wl-btn" style={{ display: 'inline-block' }}>
            Return home
          </Link>
        </div>
      </section>
    </ComingSoonLayout>
  );
};

export default Confirmed;
