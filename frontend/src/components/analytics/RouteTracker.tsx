import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

/**
 * RouteTracker
 *
 * A component that listens to route changes using `useLocation`
 * and sends page view events to Google Analytics 4 (GA4).
 * It should be placed inside the `BrowserRouter` to ensure
 * every navigation is tracked.
 */
export const RouteTracker = () => {
  const location = useLocation();

  useEffect(() => {
    // Check if gtag is available on the window object
    if (typeof window !== 'undefined' && window.gtag) {
      // Send a page_view event with the current pathname
      window.gtag('config', 'G-DV6970NSG4', {
        page_path: location.pathname + location.search,
      });
    }
  }, [location]);

  // Render nothing as this is a purely functional component
  return null;
};
