/**
 * Analytics Utility
 *
 * Provides wrapper functions for tracking custom events using Google Analytics 4 (GA4).
 * These functions ensure a consistent tracking architecture and avoid prematurely
 * instrumenting UI components directly with `gtag` calls.
 */

// Define the global gtag function type if it's not already available via types
declare global {
  interface Window {
    gtag?: (...args: any[]) => void;
  }
}

/**
 * Tracks when a user clicks the "Demo Request" button or link.
 */
export const trackDemoRequest = () => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'demo_request_clicked', {
      event_category: 'engagement',
      event_label: 'Demo Request',
    });
  }
};

/**
 * Tracks when a user successfully submits the contact form.
 */
export const trackContactSubmission = () => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'contact_form_submitted', {
      event_category: 'conversion',
      event_label: 'Contact Form',
    });
  }
};

/**
 * Tracks when a user starts the AI Audit flow.
 */
export const trackAIAuditStarted = () => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'ai_audit_started', {
      event_category: 'engagement',
      event_label: 'AI Audit',
    });
  }
};

/**
 * Tracks when a user starts the Workflow Diagnostic flow.
 */
export const trackWorkflowDiagnosticStarted = () => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'workflow_diagnostic_started', {
      event_category: 'engagement',
      event_label: 'Workflow Diagnostic',
    });
  }
};

/**
 * Tracks when a user requests early access to the Forecasting feature.
 */
export const trackForecastingEarlyAccessRequested = () => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'forecasting_early_access_requested', {
      event_category: 'conversion',
      event_label: 'Forecasting Early Access',
    });
  }
};
