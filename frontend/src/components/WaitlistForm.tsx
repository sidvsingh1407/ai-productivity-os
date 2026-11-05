import React, { useState } from 'react';
import { APP_CONFIG } from '../config/app';
import { GlassPanel } from './GlassPanel';

export const WaitlistForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [productPreference, setProductPreference] = useState('Not sure yet');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [invalidEmail, setInvalidEmail] = useState(false);
  const [emptyEmailSubmit, setEmptyEmailSubmit] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setInvalidEmail(false);
    setEmptyEmailSubmit(false);

    if (!email) {
      setEmptyEmailSubmit(true);
      return;
    }

    // basic email check
    if (!/\S+@\S+\.\S+/.test(email)) {
      setInvalidEmail(true);
      return;
    }

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

  const handleReset = () => {
    setStatus('idle');
    setEmail('');
    setProductPreference('Not sure yet');
  };

  if (status === 'success') {
    return (
      <GlassPanel className="p-6 text-center max-w-md mx-auto w-full">
        <p className="text-cs-text-primary font-medium mb-2">Thank you. Check your email to confirm.</p>
        <button
          onClick={handleReset}
          className="text-sm text-cs-text-secondary hover:text-cs-text-primary focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base rounded px-1 transition-colors"
        >
          Didn't get it? Resend.
        </button>
      </GlassPanel>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-2xl mx-auto" noValidate>
      <div className="flex flex-col md:flex-row gap-2 w-full">
        <div className="flex-grow">
          <label htmlFor="email" className="sr-only">Email address</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              setInvalidEmail(false);
              setEmptyEmailSubmit(false);
            }}
            disabled={status === 'loading'}
            className={`w-full px-4 py-3 bg-[rgba(255,255,255,0.04)] border ${invalidEmail ? 'border-red-400' : 'border-glass-border'} rounded-lg text-cs-text-primary placeholder-cs-text-muted focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base disabled:opacity-50`}
            placeholder="you@company.com"
          />
        </div>

        <div className="flex-grow md:max-w-[220px]">
          <label htmlFor="product_preference" className="sr-only">What are you most interested in?</label>
          <div className="relative">
            <select
              id="product_preference"
              value={productPreference}
              onChange={(e) => setProductPreference(e.target.value)}
              disabled={status === 'loading'}
              className="w-full px-4 py-3 bg-[rgba(255,255,255,0.04)] border border-glass-border rounded-lg text-cs-text-primary appearance-none focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base disabled:opacity-50"
            >
              <option value="Not sure yet" className="bg-cs-bg-base text-cs-text-primary">Not sure yet</option>
              <option value="Readiness" className="bg-cs-bg-base text-cs-text-primary">Readiness</option>
              <option value="Workflow" className="bg-cs-bg-base text-cs-text-primary">Workflow</option>
              <option value="Roadmap" className="bg-cs-bg-base text-cs-text-primary">Roadmap</option>
              <option value="Prompt" className="bg-cs-bg-base text-cs-text-primary">Prompt</option>
              <option value="Strategy" className="bg-cs-bg-base text-cs-text-primary">Strategy</option>
            </select>
            <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-cs-text-secondary">
              <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/>
              </svg>
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={status === 'loading'}
          className="md:w-auto w-full py-3 px-6 bg-cs-accent text-[#0A0B0F] font-semibold rounded-lg shadow-[0_0_40px_rgba(94,234,212,0.35)] hover:shadow-[0_0_60px_rgba(94,234,212,0.5)] focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base disabled:opacity-50 disabled:cursor-not-allowed transition-shadow"
        >
          {status === 'loading' ? 'Joining…' : 'Join waitlist'}
        </button>
      </div>

      <div aria-live="polite" className="text-center md:text-left min-h-[24px]">
        {invalidEmail && (
          <p className="text-red-400 text-sm">Please enter a valid email address.</p>
        )}
        {emptyEmailSubmit && (
          <p className="text-cs-text-secondary text-sm">Email cannot be empty.</p>
        )}
        {status === 'error' && (
          <p className="text-red-400 text-sm font-medium">Something went wrong. Try again.</p>
        )}
      </div>
    </form>
  );
};
