import { Link, Outlet } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import { useState } from 'react';
import { CookieBanner } from './CookieBanner';

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
              <div className="relative group">
                <button className="text-body text-text-secondary hover:text-accent-blue font-medium transition-colors flex items-center gap-1">
                  Problems
                </button>
                <div className="absolute left-0 mt-2 w-64 bg-bg-primary border border-border-light shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                  <div className="py-2">
                    <Link to="/problems/ai-roi" className="block px-4 py-2 text-sm text-text-secondary hover:bg-bg-secondary hover:text-accent-blue">AI Isn't Delivering ROI</Link>
                    <Link to="/problems/team-productivity" className="block px-4 py-2 text-sm text-text-secondary hover:bg-bg-secondary hover:text-accent-blue">Team Productivity Is Stalling</Link>
                    <Link to="/problems/operations-chaotic" className="block px-4 py-2 text-sm text-text-secondary hover:bg-bg-secondary hover:text-accent-blue">Operations Are Becoming Chaotic</Link>
                    <Link to="/problems/inconsistent-ai" className="block px-4 py-2 text-sm text-text-secondary hover:bg-bg-secondary hover:text-accent-blue">AI Outputs Are Inconsistent</Link>
                    <Link to="/problems/scale-without-hiring" className="block px-4 py-2 text-sm text-text-secondary hover:bg-bg-secondary hover:text-accent-blue">Scale Without Hiring</Link>
                  </div>
                </div>
              </div>
              <div className="relative group">
                <button className="text-body text-text-secondary hover:text-accent-blue font-medium transition-colors flex items-center gap-1">
                  Solutions
                </button>
                <div className="absolute left-0 mt-2 w-64 bg-bg-primary border border-border-light shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                  <div className="py-2">
                    <Link to="/solutions/discover-bottlenecks" className="block px-4 py-2 text-sm text-text-secondary hover:bg-bg-secondary hover:text-accent-blue">Discover Hidden Bottlenecks</Link>
                    <Link to="/solutions/improve-ai-adoption" className="block px-4 py-2 text-sm text-text-secondary hover:bg-bg-secondary hover:text-accent-blue">Improve AI Adoption</Link>
                    <Link to="/solutions/standardize-ai-outputs" className="block px-4 py-2 text-sm text-text-secondary hover:bg-bg-secondary hover:text-accent-blue">Standardize AI Outputs</Link>
                    <Link to="/solutions/reduce-manual-work" className="block px-4 py-2 text-sm text-text-secondary hover:bg-bg-secondary hover:text-accent-blue">Reduce Manual Work</Link>
                    <Link to="/solutions/improve-visibility" className="block px-4 py-2 text-sm text-text-secondary hover:bg-bg-secondary hover:text-accent-blue">Improve Operational Visibility</Link>
                  </div>
                </div>
              </div>
              <div className="relative group">
                <button className="text-body text-text-secondary hover:text-accent-blue font-medium transition-colors flex items-center gap-1">
                  Resources
                </button>
                <div className="absolute left-0 mt-2 w-56 bg-bg-primary border border-border-light shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                  <div className="py-2">
                    <Link to="/example-findings" className="block px-4 py-2 text-sm text-text-secondary hover:bg-bg-secondary hover:text-accent-blue">Example Findings</Link>
                    <Link to="/blog" className="block px-4 py-2 text-sm text-text-secondary hover:bg-bg-secondary hover:text-accent-blue">Blog / Insights</Link>
                    <Link to="/resources/guides" className="block px-4 py-2 text-sm text-text-secondary hover:bg-bg-secondary hover:text-accent-blue">Guides</Link>
                    <Link to="/resources/case-studies" className="block px-4 py-2 text-sm text-text-secondary hover:bg-bg-secondary hover:text-accent-blue">Case Studies</Link>
                    <Link to="/resources/faq" className="block px-4 py-2 text-sm text-text-secondary hover:bg-bg-secondary hover:text-accent-blue">FAQ</Link>
                    <div className="border-t border-border-light my-1"></div>
                    <Link to="/about" className="block px-4 py-2 text-sm text-text-secondary hover:bg-bg-secondary hover:text-accent-blue">About Us</Link>
                  </div>
                </div>
              </div>
              <Link to="/pricing" className="text-body text-text-secondary hover:text-accent-blue font-medium transition-colors">
                Pricing
              </Link>
            </div>

            {/* CTA */}
            <div className="hidden md:flex items-center space-x-4">
              <Link to="/login" className="text-body text-text-secondary hover:text-accent-blue font-medium transition-colors">
                Sign In
              </Link>
              <Link
                to="/register"
                className="px-4 py-2 bg-accent-blue text-text-inverse text-body font-medium rounded-md shadow-sm hover:bg-accent-blue/90 transition-colors"
              >
                Start Free Analysis
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
          <div className="md:hidden border-t border-border-light bg-bg-primary max-h-[80vh] overflow-y-auto">
            <div className="px-4 pt-2 pb-6 space-y-1">
              <div className="py-2">
                <p className="px-3 text-xs font-semibold text-text-secondary uppercase tracking-wider mb-2">Problems</p>
                <Link to="/problems/ai-roi" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 pl-6 text-sm font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">AI Isn't Delivering ROI</Link>
                <Link to="/problems/team-productivity" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 pl-6 text-sm font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Team Productivity Is Stalling</Link>
                <Link to="/problems/operations-chaotic" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 pl-6 text-sm font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Operations Are Becoming Chaotic</Link>
                <Link to="/problems/inconsistent-ai" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 pl-6 text-sm font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">AI Outputs Are Inconsistent</Link>
                <Link to="/problems/scale-without-hiring" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 pl-6 text-sm font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Scale Without Hiring</Link>
              </div>

              <div className="py-2 border-t border-border-light">
                <p className="px-3 text-xs font-semibold text-text-secondary uppercase tracking-wider mb-2">Solutions</p>
                <Link to="/solutions/discover-bottlenecks" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 pl-6 text-sm font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Discover Hidden Bottlenecks</Link>
                <Link to="/solutions/improve-ai-adoption" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 pl-6 text-sm font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Improve AI Adoption</Link>
                <Link to="/solutions/standardize-ai-outputs" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 pl-6 text-sm font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Standardize AI Outputs</Link>
                <Link to="/solutions/reduce-manual-work" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 pl-6 text-sm font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Reduce Manual Work</Link>
                <Link to="/solutions/improve-visibility" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 pl-6 text-sm font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Improve Operational Visibility</Link>
              </div>

              <div className="py-2 border-t border-border-light">
                <p className="px-3 text-xs font-semibold text-text-secondary uppercase tracking-wider mb-2">Resources</p>
                <Link to="/example-findings" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 pl-6 text-sm font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Example Findings</Link>
                <Link to="/blog" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 pl-6 text-sm font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Blog / Insights</Link>
                <Link to="/resources/guides" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 pl-6 text-sm font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Guides</Link>
                <Link to="/resources/case-studies" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 pl-6 text-sm font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Case Studies</Link>
                <Link to="/resources/faq" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 pl-6 text-sm font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">FAQ</Link>
                <Link to="/about" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 pl-6 text-sm font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">About Us</Link>
              </div>

              <Link to="/pricing" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 mt-2 text-body font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Pricing</Link>
              <Link to="/login" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-body font-medium text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Sign In</Link>

              <div className="pt-4 mt-2 border-t border-border-light">
                <p className="px-3 text-xs font-semibold text-text-secondary uppercase tracking-wider mb-2">Legal</p>
                <Link to="/privacy" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-sm text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Privacy Policy</Link>
                <Link to="/terms" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-sm text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Terms of Service</Link>
                <Link to="/cookies" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-sm text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Cookie Policy</Link>
                <Link to="/ai-disclaimer" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-sm text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">AI Disclaimer</Link>
                <Link to="/data-retention" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-sm text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Data Retention</Link>
                <Link to="/security" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-sm text-text-secondary hover:text-accent-blue hover:bg-bg-secondary rounded-md">Security</Link>
              </div>
              <Link to="/register" onClick={() => setIsMobileMenuOpen(false)} className="block mt-4 px-3 py-3 bg-accent-blue text-text-inverse text-center text-body font-medium rounded-md shadow-sm">Start Free Analysis</Link>
            </div>
          </div>
        )}
      </nav>

      {/* Main Content */}
      <main className="flex-grow">
        <Outlet />
      </main>

      {/* Global Cookie Banner */}
      <CookieBanner />

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
              <h4 className="text-body font-medium text-text-inverse mb-4">Solutions</h4>
              <ul className="space-y-3">
                <li><Link to="/solutions/discover-bottlenecks" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Discover Hidden Bottlenecks</Link></li>
                <li><Link to="/solutions/improve-ai-adoption" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Improve AI Adoption</Link></li>
                <li><Link to="/solutions/standardize-ai-outputs" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Standardize AI Outputs</Link></li>
                <li><Link to="/solutions/reduce-manual-work" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Reduce Manual Work</Link></li>
                <li><Link to="/solutions/improve-visibility" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Improve Operational Visibility</Link></li>
              </ul>
            </div>

            <div>
              <h4 className="text-body font-medium text-text-inverse mb-4">Resources</h4>
              <ul className="space-y-3">
                <li><Link to="/example-findings" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Example Findings</Link></li>
                <li><Link to="/blog" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Blog / Insights</Link></li>
                <li><Link to="/resources/guides" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Guides</Link></li>
                <li><Link to="/resources/case-studies" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Case Studies</Link></li>
                <li><Link to="/resources/faq" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">FAQ</Link></li>
                <li><Link to="/about" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">About Us</Link></li>
                <li><Link to="/contact" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Contact</Link></li>
              </ul>
            </div>

            <div>
              <h4 className="text-body font-medium text-text-inverse mb-4">Legal</h4>
              <ul className="space-y-3">
                <li><Link to="/privacy" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Privacy Policy</Link></li>
                <li><Link to="/terms" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Terms of Service</Link></li>
                <li><Link to="/cookies" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Cookie Policy</Link></li>
                <li><Link to="/ai-disclaimer" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">AI Disclaimer</Link></li>
                <li><Link to="/data-retention" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Data Retention</Link></li>
                <li><Link to="/security" className="text-body text-text-inverse/70 hover:text-accent-blue transition-colors">Security</Link></li>
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
