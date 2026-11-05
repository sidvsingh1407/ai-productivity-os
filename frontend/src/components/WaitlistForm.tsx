import React, { useState, useRef } from 'react';
import { APP_CONFIG } from '../config/app';
import { GlassPanel } from './GlassPanel';
import { ProductRadioCard } from './ProductRadioCard';

type WaitlistState = 'quick' | 'extended';
type SignupStatus = 'idle' | 'loading' | 'success' | 'error';

export const WaitlistForm: React.FC = () => {
  const [formState, setFormState] = useState<WaitlistState>('quick');
  const [email, setEmail] = useState('');

  // Extended state fields
  const [productPreference, setProductPreference] = useState<string | null>(null);
  const [companySize, setCompanySize] = useState<string | null>('1-10');
  const [problemStatement, setProblemStatement] = useState('');

  const [status, setStatus] = useState<SignupStatus>('idle');
  const [invalidEmail, setInvalidEmail] = useState(false);
  const [emptyEmailSubmit, setEmptyEmailSubmit] = useState(false);

  const emailInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setInvalidEmail(false);
    setEmptyEmailSubmit(false);

    if (!email) {
      setEmptyEmailSubmit(true);
      return;
    }

    if (!/\S+@\S+\.\S+/.test(email)) {
      setInvalidEmail(true);
      return;
    }

    setStatus('loading');

    const payload = {
      email,
      product_preference: formState === 'extended' ? productPreference : null,
      company_size: formState === 'extended' ? companySize : null,
      problem_statement: formState === 'extended' && problemStatement.trim() !== '' ? problemStatement.trim() : null,
      signup_type: formState,
      source: 'coming-soon'
    };

    try {
      const response = await fetch(`${APP_CONFIG.apiBaseUrl}/api/waitlist`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
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
    setFormState('quick');
    setProductPreference(null);
    setCompanySize('1-10');
    setProblemStatement('');
  };

  const switchToExtended = () => {
    setFormState('extended');
  };

  const switchToQuick = () => {
    setFormState('quick');
    // We defer focus so React can render the State 1 view first
    setTimeout(() => {
      emailInputRef.current?.focus();
    }, 0);
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

  if (formState === 'quick') {
    return (
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-xl mx-auto" noValidate>
        <div className="flex flex-col md:flex-row gap-2 w-full">
          <div className="flex-grow">
            <label htmlFor="email-quick" className="sr-only">Email address</label>
            <input
              type="email"
              id="email-quick"
              ref={emailInputRef}
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

          <button
            type="submit"
            disabled={status === 'loading'}
            className="md:w-auto w-full py-3 px-6 bg-cs-accent text-[#0A0B0F] font-semibold rounded-lg shadow-[0_0_40px_rgba(94,234,212,0.35)] hover:shadow-[0_0_60px_rgba(94,234,212,0.5)] focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base disabled:opacity-50 disabled:cursor-not-allowed transition-shadow"
          >
            {status === 'loading' ? 'Joining…' : 'Join waitlist'}
          </button>
        </div>

        <div className="flex justify-between items-center text-sm mt-2">
          <div aria-live="polite">
            {invalidEmail && <span className="text-red-400">Please enter a valid email address.</span>}
            {emptyEmailSubmit && <span className="text-cs-text-secondary">Email cannot be empty.</span>}
            {status === 'error' && <span className="text-red-400 font-medium">Something went wrong. Try again.</span>}
          </div>

          <button
            type="button"
            onClick={switchToExtended}
            className="text-cs-text-secondary hover:text-cs-text-primary focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base rounded px-1 transition-colors ml-auto flex items-center gap-1"
          >
            Prefer to tell us what interests you? Choose products &rarr;
          </button>
        </div>
      </form>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-8 w-full max-w-3xl mx-auto text-left" noValidate>
      <div>
        <label htmlFor="email-extended" className="block text-sm font-medium text-cs-text-primary mb-2">Email address</label>
        <input
          type="email"
          id="email-extended"
          ref={emailInputRef}
          value={email}
          onChange={(e) => {
            setEmail(e.target.value);
            setInvalidEmail(false);
            setEmptyEmailSubmit(false);
          }}
          disabled={status === 'loading'}
          className={`w-full md:max-w-md px-4 py-3 bg-[rgba(255,255,255,0.04)] border ${invalidEmail ? 'border-red-400' : 'border-glass-border'} rounded-lg text-cs-text-primary placeholder-cs-text-muted focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base disabled:opacity-50`}
          placeholder="you@company.com"
        />
        <div aria-live="polite" className="mt-1 min-h-[20px]">
          {invalidEmail && <p className="text-red-400 text-sm">Please enter a valid email address.</p>}
          {emptyEmailSubmit && <p className="text-cs-text-secondary text-sm">Email cannot be empty.</p>}
        </div>
      </div>

      <fieldset>
        <legend className="text-lg font-medium text-cs-text-primary mb-4">What are you most interested in?</legend>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" role="radiogroup">
          <ProductRadioCard
            id="readiness"
            title="Readiness"
            description="Score your AI systems against the frameworks that matter."
            selected={productPreference === 'readiness'}
            onSelect={(id) => setProductPreference(id)}
            onDeselect={() => setProductPreference(null)}
          />
          <ProductRadioCard
            id="workflow"
            title="Workflow"
            description="Find where your AI is stuck. Identify the bottlenecks and manual handoffs."
            selected={productPreference === 'workflow'}
            onSelect={(id) => setProductPreference(id)}
            onDeselect={() => setProductPreference(null)}
          />
          <ProductRadioCard
            id="roadmap"
            title="Roadmap"
            description="Starting from zero? Get a 90-day plan, tool recommendations, and a budget."
            selected={productPreference === 'roadmap'}
            onSelect={(id) => setProductPreference(id)}
            onDeselect={() => setProductPreference(null)}
          />
          <ProductRadioCard
            id="prompt"
            title="Prompt"
            description="Improve prompt quality across your team."
            selected={productPreference === 'prompt'}
            onSelect={(id) => setProductPreference(id)}
            onDeselect={() => setProductPreference(null)}
          />
          <ProductRadioCard
            id="strategy"
            title="Strategy"
            description="The strategic intelligence layer that sits on top of Readiness and Workflow."
            selected={productPreference === 'strategy'}
            onSelect={(id) => setProductPreference(id)}
            onDeselect={() => setProductPreference(null)}
          />
          <ProductRadioCard
            id="unsure"
            title="Not sure yet"
            description="Just want to stay in the loop and see what we build."
            selected={productPreference === 'unsure'}
            onSelect={(id) => setProductPreference(id)}
            onDeselect={() => setProductPreference(null)}
          />
        </div>
      </fieldset>

      <div>
        <label htmlFor="company-size" className="block text-lg font-medium text-cs-text-primary mb-4">How many people work at your company?</label>
        <div className="relative md:max-w-md">
          <select
            id="company-size"
            value={companySize || '1-10'}
            onChange={(e) => setCompanySize(e.target.value)}
            disabled={status === 'loading'}
            className="w-full px-4 py-3 bg-[rgba(255,255,255,0.04)] border border-glass-border rounded-lg text-cs-text-primary appearance-none focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base disabled:opacity-50"
          >
            <option value="1-10" className="bg-cs-bg-base text-cs-text-primary">1–10</option>
            <option value="11-50" className="bg-cs-bg-base text-cs-text-primary">11–50</option>
            <option value="51-200" className="bg-cs-bg-base text-cs-text-primary">51–200</option>
            <option value="201-1000" className="bg-cs-bg-base text-cs-text-primary">201–1000</option>
            <option value="1000+" className="bg-cs-bg-base text-cs-text-primary">1000+</option>
            <option value="prefer-not-to-say" className="bg-cs-bg-base text-cs-text-primary">Prefer not to say</option>
          </select>
          <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-cs-text-secondary">
            <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
              <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/>
            </svg>
          </div>
        </div>
      </div>

      <div>
        <label htmlFor="problem-statement" className="block text-lg font-medium text-cs-text-primary mb-2">What are you trying to solve? (optional)</label>
        <textarea
          id="problem-statement"
          value={problemStatement}
          onChange={(e) => setProblemStatement(e.target.value.slice(0, 280))}
          disabled={status === 'loading'}
          rows={3}
          maxLength={280}
          className="w-full px-4 py-3 bg-[rgba(255,255,255,0.04)] border border-glass-border rounded-lg text-cs-text-primary placeholder-cs-text-muted focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base disabled:opacity-50 resize-y"
          placeholder="I want to..."
        />
        <div className="flex justify-end mt-1 text-xs text-cs-text-muted">
          {problemStatement.length} / 280
        </div>
      </div>

      <div className="flex flex-col sm:flex-row items-center gap-6 pt-4 border-t border-glass-border">
        <button
          type="submit"
          disabled={status === 'loading'}
          className="w-full sm:w-auto py-3 px-8 bg-cs-accent text-[#0A0B0F] font-semibold rounded-lg shadow-[0_0_40px_rgba(94,234,212,0.35)] hover:shadow-[0_0_60px_rgba(94,234,212,0.5)] focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base disabled:opacity-50 disabled:cursor-not-allowed transition-shadow"
        >
          {status === 'loading' ? 'Joining…' : 'Join waitlist'}
        </button>

        <button
          type="button"
          onClick={switchToQuick}
          className="text-sm font-medium text-cs-text-secondary hover:text-cs-text-primary focus:outline-none focus:ring-2 focus:ring-cs-accent focus:ring-offset-2 focus:ring-offset-cs-bg-base rounded px-2 py-1 transition-colors"
        >
          Back to quick join
        </button>

        {status === 'error' && (
          <span className="text-red-400 text-sm font-medium ml-auto">Something went wrong. Try again.</span>
        )}
      </div>
    </form>
  );
};
