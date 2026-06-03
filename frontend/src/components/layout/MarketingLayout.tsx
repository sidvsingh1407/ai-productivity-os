import { Link, Outlet } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import { useState } from 'react';

export function MarketingLayout() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-foreground/10 flex flex-col">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 w-full bg-background/95 backdrop-blur-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            {/* Logo */}
            <div className="flex-shrink-0 flex items-center">
              <Link to="/" className="text-xl font-medium tracking-tight text-foreground flex items-center gap-2">
                <span className="w-4 h-4 bg-foreground block rounded-sm"></span>
                TarkaX
              </Link>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-8">
              <Link to="/ai-audit" className="text-sm text-gray-600 hover:text-foreground font-medium transition-colors">
                AI Audit
              </Link>
              <Link to="/workflow-diagnostic" className="text-sm text-gray-600 hover:text-foreground font-medium transition-colors">
                Workflow Diagnostic
              </Link>
              <Link to="/forecasting" className="text-sm text-gray-600 hover:text-foreground font-medium transition-colors">
                Forecasting
              </Link>
              <Link to="/about" className="text-sm text-gray-600 hover:text-foreground font-medium transition-colors">
                About
              </Link>
              <Link to="/blog" className="text-sm text-gray-600 hover:text-foreground font-medium transition-colors">
                Blog
              </Link>
            </div>

            {/* CTA */}
            <div className="hidden md:flex items-center space-x-4">
              <Link to="/login" className="text-sm text-gray-600 hover:text-foreground font-medium transition-colors">
                Sign In
              </Link>
              <Link
                to="/contact"
                className="px-4 py-2 bg-foreground text-background text-sm font-medium rounded hover:bg-foreground/90 transition-colors"
              >
                Request a Demo
              </Link>
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden flex items-center">
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="text-gray-500 hover:text-foreground p-2"
              >
                {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t border-gray-100 bg-background">
            <div className="px-4 pt-2 pb-6 space-y-1">
              <Link to="/ai-audit" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-base font-medium text-gray-600 hover:text-foreground hover:bg-gray-50 rounded-md">AI Audit</Link>
              <Link to="/workflow-diagnostic" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-base font-medium text-gray-600 hover:text-foreground hover:bg-gray-50 rounded-md">Workflow Diagnostic</Link>
              <Link to="/forecasting" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-base font-medium text-gray-600 hover:text-foreground hover:bg-gray-50 rounded-md">Forecasting</Link>
              <Link to="/about" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-base font-medium text-gray-600 hover:text-foreground hover:bg-gray-50 rounded-md">About</Link>
              <Link to="/blog" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-base font-medium text-gray-600 hover:text-foreground hover:bg-gray-50 rounded-md">Blog</Link>
              <Link to="/login" onClick={() => setIsMobileMenuOpen(false)} className="block px-3 py-2 text-base font-medium text-gray-600 hover:text-foreground hover:bg-gray-50 rounded-md">Sign In</Link>
              <Link to="/contact" onClick={() => setIsMobileMenuOpen(false)} className="block mt-4 px-3 py-3 bg-foreground text-background text-center text-base font-medium rounded-md">Request a Demo</Link>
            </div>
          </div>
        )}
      </nav>

      {/* Main Content */}
      <main className="flex-grow">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-background border-t border-gray-200 py-16 mt-auto">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
            <div className="col-span-1 md:col-span-1">
              <Link to="/" className="text-xl font-medium tracking-tight text-foreground flex items-center gap-2 mb-4">
                <span className="w-4 h-4 bg-foreground block rounded-sm"></span>
                TarkaX
              </Link>
              <p className="text-sm text-gray-500 font-light leading-relaxed">
                Operational Intelligence Platform built on Failure Intelligence principles.
              </p>
            </div>

            <div>
              <h4 className="font-medium text-foreground mb-4">Platform</h4>
              <ul className="space-y-3">
                <li><Link to="/ai-audit" className="text-sm text-gray-500 hover:text-foreground transition-colors">AI Audit</Link></li>
                <li><Link to="/workflow-diagnostic" className="text-sm text-gray-500 hover:text-foreground transition-colors">Workflow Diagnostic</Link></li>
                <li><Link to="/forecasting" className="text-sm text-gray-500 hover:text-foreground transition-colors">Forecasting <span className="text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded ml-1">Soon</span></Link></li>
              </ul>
            </div>

            <div>
              <h4 className="font-medium text-foreground mb-4">Company</h4>
              <ul className="space-y-3">
                <li><Link to="/about" className="text-sm text-gray-500 hover:text-foreground transition-colors">About</Link></li>
                <li><Link to="/blog" className="text-sm text-gray-500 hover:text-foreground transition-colors">Research & Insights</Link></li>
                <li><Link to="/contact" className="text-sm text-gray-500 hover:text-foreground transition-colors">Contact</Link></li>
              </ul>
            </div>

            <div>
              <h4 className="font-medium text-foreground mb-4">Legal</h4>
              <ul className="space-y-3">
                <li><span className="text-sm text-gray-500">Privacy Policy</span></li>
                <li><span className="text-sm text-gray-500">Terms of Service</span></li>
              </ul>
            </div>
          </div>

          <div className="pt-8 border-t border-gray-100 flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-gray-400">© {new Date().getFullYear()} TarkaX. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
