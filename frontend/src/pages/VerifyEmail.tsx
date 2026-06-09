import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { apiClient } from '../lib/api';

export function VerifyEmail() {
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [errorMessage, setErrorMessage] = useState('');

  const location = useLocation();

  useEffect(() => {
    const verifyToken = async () => {
      const params = new URLSearchParams(location.search);
      const token = params.get('token');

      if (!token) {
        setStatus('error');
        setErrorMessage('No verification token provided.');
        return;
      }

      try {
        await apiClient.post('/api/auth/verify-email', { token });
        setStatus('success');
      } catch (error: any) {
        setStatus('error');
        setErrorMessage(error.message || 'Verification failed. The link may have expired or is invalid.');
      }
    };

    verifyToken();
  }, [location]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8" style={{ background: 'var(--tx-bg-background)' }}>
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow-sm border text-center" style={{ borderColor: 'var(--tx-border)', background: 'var(--tx-bg-card)' }}>

        <h2 className="mt-6 text-3xl font-extrabold" style={{ color: 'var(--tx-text-primary)' }}>
          Email Verification
        </h2>

        {status === 'loading' && (
          <div className="mt-4">
            <p className="text-sm" style={{ color: 'var(--tx-text-secondary)' }}>Verifying your email address...</p>
            {/* Simple spinner */}
            <div className="mt-4 flex justify-center">
              <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
          </div>
        )}

        {status === 'success' && (
          <div className="mt-4">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
              <svg className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <p className="mt-4 text-sm" style={{ color: 'var(--tx-text-secondary)' }}>
              Your email address has been successfully verified! You can now access all features.
            </p>
            <div className="mt-6">
              <Link to="/app/dashboard" className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700" style={{ background: 'var(--tx-button-primary)', color: 'var(--tx-button-primary-text)' }}>
                Go to Dashboard
              </Link>
            </div>
          </div>
        )}

        {status === 'error' && (
          <div className="mt-4">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
              <svg className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <p className="mt-4 text-sm text-red-600">
              {errorMessage}
            </p>
            <div className="mt-6 space-y-3">
              <Link to="/app/dashboard" className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700" style={{ background: 'var(--tx-button-primary)', color: 'var(--tx-button-primary-text)' }}>
                Continue to Dashboard
              </Link>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
