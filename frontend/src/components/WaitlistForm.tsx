import React, { useState, useRef } from 'react';
import { APP_CONFIG } from '../config/app';

type WaitlistState = 'quick' | 'extended';
type SignupStatus = 'idle' | 'loading' | 'success' | 'error';

const PRODUCTS = [
  { id: 'readiness', title: 'Readiness', description: 'Score your AI systems against the frameworks that matter.' },
  { id: 'workflow', title: 'Workflow', description: 'Find where your AI is stuck. Identify the bottlenecks and manual handoffs.' },
  { id: 'roadmap', title: 'Roadmap', description: 'Starting from zero? Get a 90-day plan, tool recommendations, and a budget.' },
  { id: 'prompt', title: 'Prompt', description: 'Improve prompt quality across your team.' },
  { id: 'strategy', title: 'Strategy', description: 'The strategic intelligence layer that sits on top of Readiness and Workflow.' },
  { id: 'unsure', title: 'Not sure yet', description: 'Just want to stay in the loop and see what we build.' },
];

interface WaitlistFormProps {
  variant?: 'hero' | 'page';
}

export const WaitlistForm: React.FC<WaitlistFormProps> = ({ variant = 'page' }) => {
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

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
    setInvalidEmail(false);
    setEmptyEmailSubmit(false);
  };

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
    setTimeout(() => {
      emailInputRef.current?.focus();
    }, 0);
  };

  if (status === 'success') {
    return (
      <div className="wl-form">
        <p style={{ fontFamily: 'var(--tk-font-primary)', fontSize: '18px', color: variant === 'hero' ? '#ffffff' : '#000000' }}>
          Thank you. Check your email to confirm.
        </p>
        <button onClick={handleReset} className="wl-link">
          Didn't get it? Resend.
        </button>
      </div>
    );
  }

  if (formState === 'quick') {
    return (
      <form onSubmit={handleSubmit} className="wl-form" noValidate>
        <div>
          <label htmlFor="wl-email" className="wl-label">Email address</label>
          <input
            id="wl-email"
            ref={emailInputRef}
            type="email"
            value={email}
            onChange={handleEmailChange}
            disabled={status === 'loading'}
            className="wl-input"
            placeholder="you@company.com"
          />
        </div>
        <button
          type="submit"
          className={`wl-btn${variant === 'hero' ? ' wl-btn--dark' : ''}`}
          disabled={status === 'loading'}
        >
          {status === 'loading' ? 'Joining…' : 'Join waitlist'}
        </button>
        {invalidEmail && <p className="wl-error">Please enter a valid email address.</p>}
        {emptyEmailSubmit && <p className="wl-error">Email cannot be empty.</p>}
        {status === 'error' && <p className="wl-error">Something went wrong. Try again.</p>}
        <button type="button" className="wl-link" onClick={switchToExtended}
          style={variant === 'hero' ? { color: 'rgba(255,255,255,0.7)' } : {}}>
          Choose products →
        </button>
      </form>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="wl-form" noValidate>
      <div>
        <label htmlFor="wl-email" className="wl-label">Email address</label>
        <input id="wl-email" ref={emailInputRef} type="email" value={email}
          onChange={handleEmailChange} className="wl-input" placeholder="you@company.com" />
      </div>

      <fieldset className="wl-fieldset">
        <legend className="wl-label">What are you most interested in?</legend>
        {PRODUCTS.map((p) => (
          <label key={p.id} className="wl-option">
            <input
              type="radio"
              name="product"
              value={p.id}
              checked={productPreference === p.id}
              onChange={() => setProductPreference(p.id)}
              className="wl-radio"
            />
            <span className="wl-radio-dot" aria-hidden="true" />
            <span className="wl-option-body">
              <span className="wl-option-name">{p.title}</span>
              <span className="wl-option-copy">{p.description}</span>
            </span>
          </label>
        ))}
      </fieldset>

      <div>
        <label htmlFor="wl-size" className="wl-label">How many people work at your company?</label>
        <select id="wl-size" value={companySize || '1-10'}
          onChange={(e) => setCompanySize(e.target.value)} className="wl-select">
          <option value="1-10">1–10</option>
          <option value="11-50">11–50</option>
          <option value="51-200">51–200</option>
          <option value="201-1000">201–1000</option>
          <option value="1000+">1000+</option>
          <option value="prefer-not-to-say">Prefer not to say</option>
        </select>
      </div>

      <div>
        <label htmlFor="wl-problem" className="wl-label">What are you trying to solve? (optional)</label>
        <textarea id="wl-problem" value={problemStatement}
          onChange={(e) => setProblemStatement(e.target.value.slice(0, 280))}
          className="wl-textarea" rows={3}
          placeholder='For example: "We have three AI tools and no idea if we are compliant."' />
        <p className="wl-counter">{problemStatement.length}/280</p>
      </div>

      <button type="submit" className="wl-btn" disabled={status === 'loading'}>
        {status === 'loading' ? 'Joining…' : 'Join waitlist'}
      </button>
      {invalidEmail && <p className="wl-error">Please enter a valid email address.</p>}
      {emptyEmailSubmit && <p className="wl-error">Email cannot be empty.</p>}
      {status === 'error' && <p className="wl-error">Something went wrong. Try again.</p>}
      <button type="button" className="wl-link" onClick={switchToQuick}>Back</button>
    </form>
  );
};
