import React, { useState } from 'react';
import { APP_CONFIG } from '../config/app';

export const WaitlistForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [productPreference, setProductPreference] = useState('Not sure yet');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;

    setStatus('loading');

    try {
      const response = await fetch(`${APP_CONFIG.apiBaseUrl}/api/waitlist`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          product_preference: productPreference,
          source: 'coming_soon_page',
        }),
      });

      if (response.ok) {
        setStatus('success');
      } else {
        setStatus('error');
      }
    } catch (err) {
      setStatus('error');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-md mx-auto mt-8">
      <div className="flex flex-col gap-1">
        <label htmlFor="email" className="text-sm font-medium text-gray-700">Email address</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          disabled={status === 'loading'}
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-black focus:border-black disabled:opacity-50"
          placeholder="you@company.com"
        />
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="product_preference" className="text-sm font-medium text-gray-700">What are you most interested in?</label>
        <select
          id="product_preference"
          value={productPreference}
          onChange={(e) => setProductPreference(e.target.value)}
          disabled={status === 'loading'}
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-black focus:border-black disabled:opacity-50"
        >
          <option value="Not sure yet">Not sure yet</option>
          <option value="Readiness">Readiness</option>
          <option value="Workflow">Workflow</option>
          <option value="Roadmap">Roadmap</option>
          <option value="Prompt">Prompt</option>
          <option value="Strategy">Strategy</option>
        </select>
      </div>

      <button
        type="submit"
        disabled={status === 'loading'}
        className="w-full py-2 px-4 bg-black text-white font-medium rounded-md hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-black disabled:opacity-50 mt-2"
      >
        {status === 'loading' ? 'Submitting...' : 'Join waitlist'}
      </button>

      <div aria-live="polite" className="mt-2 text-center h-6">
        {status === 'success' && (
          <p className="text-green-700 text-sm font-medium">Thank you. Check your email to confirm.</p>
        )}
        {status === 'error' && (
          <p className="text-red-600 text-sm font-medium">Something went wrong. Try again.</p>
        )}
      </div>
    </form>
  );
};
