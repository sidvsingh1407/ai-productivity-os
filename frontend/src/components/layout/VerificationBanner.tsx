import { useState } from 'react';
import { useAuthStore } from '../../store/authStore';
import { apiClient } from '../../lib/api';

export function VerificationBanner() {
  const { user } = useAuthStore();
  const [dismissed, setDismissed] = useState(false);
  const [resendStatus, setResendStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  // Simple check since email_verified is now in DB schema, ensure it's in user object
  // If user object doesn't have it yet or it's true, we don't show the banner.
  const isVerified = user?.email_verified !== false;

  if (isVerified || dismissed) {
    return null;
  }

  const handleResend = async () => {
    setResendStatus('loading');
    try {
      await apiClient.post('/api/auth/resend-verification', { email: user?.email });
      setResendStatus('success');
      setTimeout(() => setResendStatus('idle'), 5000);
    } catch (error) {
      setResendStatus('error');
      setTimeout(() => setResendStatus('idle'), 5000);
    }
  };

  return (
    <div className="bg-indigo-600 relative" style={{ background: 'var(--tx-bg-inverted)' }}>
      <div className="max-w-7xl mx-auto py-3 px-3 sm:px-6 lg:px-8">
        <div className="pr-16 sm:text-center sm:px-16">
          <p className="font-medium text-white">
            <span className="md:hidden" style={{ color: 'var(--tx-text-inverted)' }}>Please verify your email.</span>
            <span className="hidden md:inline" style={{ color: 'var(--tx-text-inverted)' }}>
              Please verify your email address to ensure your account is secure.
            </span>
            <span className="block sm:ml-2 sm:inline-block">
              {resendStatus === 'success' ? (
                <span className="text-green-300 font-bold ml-2">Verification email sent!</span>
              ) : (
                <button
                  onClick={handleResend}
                  disabled={resendStatus === 'loading'}
                  className="text-white font-bold underline ml-2 hover:text-indigo-200 disabled:opacity-50"
                  style={{ color: 'var(--tx-text-inverted)' }}
                >
                  {resendStatus === 'loading' ? 'Sending...' : 'Resend verification email'}
                </button>
              )}
            </span>
          </p>
        </div>
        <div className="absolute inset-y-0 right-0 pt-1 pr-1 flex items-start sm:pt-1 sm:pr-2 sm:items-start">
          <button
            type="button"
            onClick={() => setDismissed(true)}
            className="flex p-2 rounded-md hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-white"
          >
            <span className="sr-only">Dismiss</span>
            <svg className="h-6 w-6 text-white" style={{ color: 'var(--tx-text-inverted)' }} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
