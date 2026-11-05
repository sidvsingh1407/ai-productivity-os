import React from 'react';
import { BackdropGradients } from './BackdropGradients';
import { GlassPanel } from './GlassPanel';
import { Link } from 'react-router-dom';

interface ComingSoonLayoutProps {
  children: React.ReactNode;
  isShell?: boolean;
}

export const ComingSoonLayout: React.FC<ComingSoonLayoutProps> = ({ children, isShell = false }) => {
  return (
    <div className="min-h-screen bg-cs-bg-base text-cs-text-primary font-sans selection:bg-cs-accent selection:text-cs-bg-base flex flex-col relative overflow-hidden">
      <BackdropGradients />

      <div className="relative z-10 flex-grow max-w-[720px] w-full mx-auto px-6 pt-24 md:pt-32 pb-20 flex flex-col justify-between h-full min-h-screen">
        <main className="w-full flex-grow flex flex-col">
          {isShell ? (
            <GlassPanel className="p-8 w-full shadow-subtle my-auto">
              {children}
            </GlassPanel>
          ) : (
            children
          )}
        </main>

        {/* Footer */}
        <footer className="mt-24">
          <GlassPanel className="p-6 w-full flex flex-col gap-6">
            <div className="flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-cs-text-secondary">
              <div className="flex flex-col md:flex-row md:items-center gap-4">
                <span>&copy; 2026 Tarkaya</span>
                <a href="mailto:privacy@tarkaya.com" className="hover:text-cs-text-primary focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base rounded px-1 transition-colors">
                  privacy@tarkaya.com
                </a>
              </div>
              <div className="flex gap-4 flex-wrap">
                <Link to="/privacy" className="hover:text-cs-text-primary focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base rounded px-1 transition-colors">Privacy</Link>
                <Link to="/terms" className="hover:text-cs-text-primary focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base rounded px-1 transition-colors">Terms of Service</Link>
                <Link to="/contact" className="hover:text-cs-text-primary focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base rounded px-1 transition-colors">Contact</Link>
                <Link to="/dpa" className="hover:text-cs-text-primary focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base rounded px-1 transition-colors">Data Processing Agreement</Link>
                <Link to="/subprocessors" className="hover:text-cs-text-primary focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base rounded px-1 transition-colors">Subprocessors</Link>
              </div>
            </div>
            <div className="text-center text-sm text-cs-text-muted">
              We are building toward ISO 27001 certification. Not yet certified.
            </div>
          </GlassPanel>
        </footer>
      </div>
    </div>
  );
};
