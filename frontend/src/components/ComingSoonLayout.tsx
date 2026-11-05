import React from 'react';
import { Link } from 'react-router-dom';
import { BrandHeader } from './BrandHeader';

interface ComingSoonLayoutProps {
  children: React.ReactNode;
}

export const ComingSoonLayout: React.FC<ComingSoonLayoutProps> = ({ children }) => {
  return (
    <div className="cs-root">
      <BrandHeader />
      <main>{children}</main>
      <footer className="cs-footer">
        <div className="cs-footer-inner">
          <span className="cs-footer-brand">TARKAYA</span>
          <a href="mailto:privacy@tarkaya.com" className="cs-footer-email">
            privacy@tarkaya.com
          </a>
          <nav className="cs-footer-nav">
            <Link to="/privacy">Privacy</Link>
            <Link to="/terms">Terms</Link>
            <Link to="/contact">Contact</Link>
          </nav>
        </div>
      </footer>
    </div>
  );
};
