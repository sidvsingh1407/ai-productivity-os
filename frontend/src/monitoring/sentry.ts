import * as Sentry from '@sentry/react';

const SENSITIVE_KEYS = new Set([
  'password',
  'secret',
  'token',
  'authorization',
  'cookie',
  'jwt',
  'api_key',
  'apikey',
  'access_token',
  'refresh_token',
  'verification_token',
  'signature',
  'email_contents',
]);

function scrubSensitiveData(event: Sentry.Event) {
  if (event.request) {
    if (event.request.headers) {
      for (const key of Object.keys(event.request.headers)) {
        if (SENSITIVE_KEYS.has(key.toLowerCase())) {
          event.request.headers[key] = '[Filtered]';
        }
      }
    }

    if (event.request.cookies) {
      for (const key of Object.keys(event.request.cookies)) {
        event.request.cookies[key] = '[Filtered]';
      }
    }

    if (event.request.data && typeof event.request.data === 'object') {
      const data = event.request.data as Record<string, any>;
      for (const key of Object.keys(data)) {
        if (SENSITIVE_KEYS.has(key.toLowerCase())) {
          data[key] = '[Filtered]';
        }
      }
    }
  }

  return event;
}

export function initSentry() {
  const dsn = import.meta.env.VITE_SENTRY_DSN;

  if (!dsn) {
    console.log('SENTRY_DSN is not set. Sentry monitoring is disabled.');
    return false;
  }

  try {
    const environment = import.meta.env.VITE_SENTRY_ENVIRONMENT || import.meta.env.VITE_APP_ENVIRONMENT || 'development';
    const release = import.meta.env.VITE_SENTRY_RELEASE;

    Sentry.init({
      dsn,
      environment,
      release: release || undefined,
      beforeSend: scrubSensitiveData,
      tracesSampleRate: 0.0,
      replaysSessionSampleRate: 0.0,
      replaysOnErrorSampleRate: 0.0,
      sendDefaultPii: false,
    });

    console.log(`Sentry initialized for environment: ${environment}`);
    return true;
  } catch (error) {
    console.error('Failed to initialize Sentry:', error);
    return false;
  }
}
