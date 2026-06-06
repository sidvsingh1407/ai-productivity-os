import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

export function CookieBanner() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const consent = localStorage.getItem('cookie_consent');
    if (!consent) {
      setIsVisible(true);
    }
  }, []);

  const handleAccept = () => {
    localStorage.setItem('cookie_consent', 'accepted');
    setIsVisible(false);
  };

  const handleReject = () => {
    localStorage.setItem('cookie_consent', 'rejected');
    setIsVisible(false);
  };

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 bg-bg-secondary border-t border-border-light shadow-lg">
      <div className="max-w-7xl mx-auto p-4 sm:p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="text-body text-text-secondary">
          We use cookies to improve your experience on our platform.
          By continuing to use our site, you agree to our use of cookies.
        </div>
        <div className="flex items-center gap-3 shrink-0">
          <Link
            to="/cookies"
            className="text-body font-medium text-brand-primary hover:underline whitespace-nowrap"
          >
            Learn More
          </Link>
          <button
            onClick={handleReject}
            className="px-4 py-2 text-sm font-medium text-text-secondary bg-bg-primary border border-border-light rounded hover:bg-bg-secondary transition-colors"
          >
            Reject
          </button>
          <button
            onClick={handleAccept}
            className="px-4 py-2 text-sm font-medium text-white bg-accent-blue rounded hover:bg-accent-blue/90 transition-colors"
          >
            Accept
          </button>
        </div>
      </div>
    </div>
  );
}
