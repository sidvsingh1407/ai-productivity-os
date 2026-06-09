import { useState } from 'react';
import { Link } from 'react-router-dom';
import { authApi } from '@/api/auth';

export function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');
    setErrorMessage('');

    try {
      await authApi.forgotPassword({ email });
      setStatus('success');
    } catch (error: any) {
      setStatus('error');
      setErrorMessage(error.message || 'Failed to request password reset. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8" style={{ background: 'var(--tx-bg-background)' }}>
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow-sm border" style={{ borderColor: 'var(--tx-border)', background: 'var(--tx-bg-card)' }}>
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold" style={{ color: 'var(--tx-text-primary)' }}>
            Reset your password
          </h2>
          <p className="mt-2 text-center text-sm" style={{ color: 'var(--tx-text-secondary)' }}>
            Enter your email address and we'll send you a link to reset your password.
          </p>
        </div>

        {status === 'success' ? (
          <div className="rounded-md bg-green-50 p-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-green-800">Check your email</h3>
                <div className="mt-2 text-sm text-green-700">
                  <p>If an account exists with {email}, we've sent instructions for resetting your password.</p>
                </div>
                <div className="mt-4">
                  <Link to="/login" className="text-sm font-medium text-green-800 hover:text-green-900 underline">
                    Return to login
                  </Link>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            {status === 'error' && (
              <div className="rounded-md bg-red-50 p-4">
                <div className="flex">
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">{errorMessage}</h3>
                  </div>
                </div>
              </div>
            )}

            <div className="rounded-md shadow-sm -space-y-px">
              <div>
                <label htmlFor="email-address" className="sr-only">Email address</label>
                <input
                  id="email-address"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="Email address"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={status === 'loading'}
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                style={{ background: 'var(--tx-button-primary)', color: 'var(--tx-button-primary-text)' }}
              >
                {status === 'loading' ? 'Sending...' : 'Send reset instructions'}
              </button>
            </div>

            <div className="text-center mt-4">
              <Link to="/login" className="font-medium text-indigo-600 hover:text-indigo-500 text-sm">
                Back to login
              </Link>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
