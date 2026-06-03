import { Link, Outlet } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import { useState } from 'react';

export function MarketingLayout() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-bg-primary text-text-primary font-sans selection:bg-accent-blue/10 flex flex-col">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 w-full bg-bg-primary shadow-subtle border-b border-border-light transition-shadow duration-300">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            {/* Logo */}
            <div className="flex-shrink-0 flex items-center">
              <Link to="/" className="text-h3 text-text-primary flex items-center gap-2">
                <span className="w-4 h-4 bg-text-primary block rounded-sm"></span>
                TarkaX
              </Link>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-8">
              <Link to="/ai-audit" className="text-body text-text-secondary hover:text-accent-blue font-medium transition-colors">
                AI Audit
              </Link>
              <Link to="/workflow-diagnostic" className="text-body text-text-secondary hover:text-accent-blue font-medium transition-colors">
                Workflow Diagnostic
              </Link>
              <Link to="/forecasting" className="text-body text-text-secondary hover:text-accent-blue font-medium transition-colors">
                Forecasting
              </Link>
              <Link to="/about" className="text-body text-text-secondary hover:text-accent-blue font-medium transition-colors">
                About
              </Link>
              <Link to="#" className="text-body font-medium text-text-secondary hover:text-accent-blue transition-colors flex items-center gap-2">
                Methodology
                <span className="text-[10px] bg-bg-secondary border border-border-light text-text-secondary px-1.5 py-0.5 rounded uppercase tracking-wider font-mono">Coming Soon</span>
              </Link>
              <Link to="/blog" className="text-body text-text-secondary hover:text-accent-blue font-medium transition-colors">
                Blog
              </Link>
            </div>

            {/* CTA */}
            <div className="hidden md:flex items-center space-x-4">
              <Link to="/login" className="text-body text-text-secondary hover:text-accent-blue font-medium transition-colors">
                Sign In
              </Link>
              <Link
                to="/contact"
                className="px-4 py-2 bg-accent-blue text-text-inverse text-body font-medium rounded-md shadow-sm hover:bg-accent-blue/90 transition-colors"
              >
                Request a Demo
              </Link>
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden flex items-center">
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="text-text-secondary hover:text-accent-blue p-2"
              >
                {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t border-border-light bg-bg-primary">
            <div className="px-4 pt-2 pb-6 space-y-1">
              <Link to="/ai-audit" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-body font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">AI Audit</Link>
              <Link to="/workflow-diagnostic" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-body font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Workflow Diagnostic</Link>
              <Link to="/forecasting" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-body font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Forecasting</Link>
              <Link to="/about" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-body font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">About</Link>
              <Link to="#" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-body font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md flex items-center justify-between">
                Methodology
                <span className="text-[10px] bg-bg-secondary border border-border-light text-text-secondary px-1.5 py-0.5 rounded uppercase tracking-wider font-mono">Coming Soon</span>
              </Link>
              <Link to="/blog" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-body font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Blog</Link>
              <Link to="/login" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-body font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Sign In</Link>
              <Link to="/contact" onClick={() => setIsMobileMenuOpen(false)} className="block mt-4 px-3 py-3 bg-accent-blue text-text-inverse text-center text-body font-medium rounded-md shadow-sm">Request a Demo</Link>
            </div>
          </div>
        )}
      </nav>

      {/* Main Content */}
      <main className="flex-grow">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-bg-dark border-t border-border-strong py-space-xl mt-auto text-text-inverse">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-space-lg mb-space-lg">
            <div className="col-span-1 md:col-span-1">
              <Link to="/" className="text-h3 text-text-inverse flex items-center gap-2 mb-4">
                <span className="w-4 h-4 bg-text-inverse block rounded-sm"></span>
                TarkaX
              </Link>
              <p className="text-body text-text-inverse/70 font-light leading-relaxed">
                Operational Intelligence Platform built on Failure Intelligence principles.
              </p>
            </div>

            <div>
              <h4 className="text-body font-medium text-text-inverse mb-4">Platform</h4>
              <ul className="space-y-3">
                <li><Link to="/ai-audit" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">AI Audit</Link></li>
                <li><Link to="/workflow-diagnostic" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Workflow Diagnostic</Link></li>
                <li><Link to="/forecasting" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors flex items-center gap-2">Forecasting <span className="text-label bg-text-inverse/10 text-text-inverse px-1.5 py-0.5 rounded">Soon</span></Link></li>
              </ul>
            </div>

            <div>
              <h4 className="text-body font-medium text-text-inverse mb-4">Company</h4>
              <ul className="space-y-3">
                <li><Link to="/about" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">About</Link></li>
                <li>
                  <Link to="#" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors inline-flex items-center gap-2">
                    Methodology
                    <span className="text-[10px] bg-text-inverse/10 text-text-inverse/70 px-1.5 py-0.5 rounded uppercase tracking-wider font-mono">Coming Soon</span>
                  </Link>
                </li>
                <li><Link to="/blog" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Research & Insights</Link></li>
                <li><Link to="/contact" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Contact</Link></li>
              </ul>
            </div>

            <div>
              <h4 className="text-body font-medium text-text-inverse mb-4">Legal</h4>
              <ul className="space-y-3">
                <li><span className="text-body text-text-inverse/70">Privacy Policy</span></li>
                <li><span className="text-body text-text-inverse/70">Terms of Service</span></li>
              </ul>
            </div>
          </div>

          <div className="pt-8 border-t border-text-inverse/10 flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-body text-text-inverse/50">© {new Date().getFullYear()} TarkaX. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
