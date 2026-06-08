import { Link } from 'react-router-dom';
import { SeoHead } from '../../../components/geo/SeoHead';
import { ArrowRight, CheckCircle2, AlertTriangle } from 'lucide-react';

interface ProblemTemplateProps {
  title: string;
  seoTitle: string;
  description: string;
  symptoms: string[];
  hiddenCauses: string[];
  findingExample: {
    stat: string;
    description: string;
    impact: string;
  };
  productLensUrl: string;
  productLensLabel: string;
}

export function ProblemTemplate({
  title,
  seoTitle,
  description,
  symptoms,
  hiddenCauses,
  findingExample,
  productLensUrl,
  productLensLabel
}: ProblemTemplateProps) {
  return (
    <div className="bg-bg-primary">
      <SeoHead
        title={`${seoTitle} | TarkaX`}
        description={description}
        canonical={`https://tarkax.com/problems/${seoTitle.toLowerCase().replace(/ /g, '-')}`}
      />

      {/* Hero */}
      <section className="py-24 bg-bg-primary border-b border-border-strong">
        <div className="max-w-4xl mx-auto px-6 lg:px-8 text-center">
          <h1 className="text-display text-text-primary mb-6">{title}</h1>
          <p className="text-h3 font-normal text-text-secondary mb-12">{description}</p>
          <Link
            to="/register"
            className="px-8 py-4 bg-accent-blue text-text-inverse text-body font-medium transition-colors hover:bg-accent-blue/90 inline-flex items-center justify-center rounded-md shadow-sm"
          >
            Start Free Analysis
          </Link>
        </div>
      </section>

      {/* Symptoms vs Causes */}
      <section className="py-24 bg-bg-secondary border-b border-border-strong">
        <div className="max-w-6xl mx-auto px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
            <div>
              <h3 className="text-h2 text-text-primary mb-6 flex items-center gap-3">
                <AlertTriangle className="text-accent-amber" /> What You See (Symptoms)
              </h3>
              <ul className="space-y-4">
                {symptoms.map((symptom, i) => (
                  <li key={i} className="flex items-start gap-3 text-body text-text-secondary bg-bg-primary p-4 rounded border border-border-light shadow-sm">
                    <span className="w-2 h-2 mt-2 bg-accent-amber rounded-full shrink-0"></span>
                    {symptom}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="text-h2 text-text-primary mb-6 flex items-center gap-3">
                <CheckCircle2 className="text-accent-blue" /> What's Actually Happening
              </h3>
              <ul className="space-y-4">
                {hiddenCauses.map((cause, i) => (
                  <li key={i} className="flex items-start gap-3 text-body text-text-secondary bg-bg-primary p-4 rounded border border-border-light shadow-sm">
                    <span className="w-2 h-2 mt-2 bg-accent-blue rounded-full shrink-0"></span>
                    {cause}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Example Finding */}
      <section className="py-24 bg-bg-primary border-b border-border-strong">
        <div className="max-w-4xl mx-auto px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-h2 text-text-primary mb-4">What TarkaX Reveals</h2>
            <p className="text-body text-text-secondary">An example of the findings our diagnostic tools uncover.</p>
          </div>
          <div className="border border-border-strong bg-bg-secondary p-8 rounded-lg shadow-sm">
            <div className="text-xs font-mono text-accent-red mb-4">EXAMPLE FINDING</div>
            <h3 className="text-2xl font-bold text-text-primary mb-4">{findingExample.stat}</h3>
            <p className="text-body text-text-secondary mb-6 border-b border-border-light pb-6">{findingExample.description}</p>
            <div>
              <div className="text-xs text-text-secondary uppercase mb-1">Business Impact</div>
              <div className="font-medium text-text-primary">{findingExample.impact}</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 bg-bg-dark text-center text-text-inverse">
        <div className="max-w-3xl mx-auto px-6 lg:px-8">
          <h2 className="text-display mb-6">Stop Guessing. Start Knowing.</h2>
          <p className="text-h3 font-normal text-text-inverse/80 mb-12">
            Discover what's actually slowing growth before you spend more money on tools, consultants, or hiring.
          </p>
          <Link
            to={productLensUrl}
            className="inline-flex items-center justify-center px-8 py-4 bg-accent-blue text-text-inverse text-body font-medium transition-colors hover:bg-accent-blue/90 rounded-md shadow-sm gap-2"
          >
            {productLensLabel} <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  );
}
