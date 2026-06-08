import { Link } from 'react-router-dom';
import { SeoHead } from '../../components/geo/SeoHead';
import { CheckCircle2 } from 'lucide-react';

export default function PricingPage() {
  return (
    <div className="bg-bg-primary min-h-screen">
      <SeoHead
        title="Pricing | TarkaX"
        description="Transparent pricing based on operational outcomes, not features. Find the right plan to uncover your business bottlenecks."
        canonical="https://tarkax.com/pricing"
      />

      {/* Header */}
      <section className="py-24 bg-bg-primary text-center px-6 lg:px-8 border-b border-border-strong">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-display text-text-primary mb-6">Invest in Clarity</h1>
          <p className="text-h3 font-normal text-text-secondary">
            Stop paying for tools that don't get used. Start investing in knowing exactly what your business needs to scale.
          </p>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="py-24 bg-bg-secondary px-6 lg:px-8 border-b border-border-strong">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">

            {/* Starter */}
            <div className="bg-bg-primary border border-border-strong rounded-xl p-8 shadow-sm flex flex-col">
              <div className="mb-8">
                <h3 className="text-2xl font-bold text-text-primary mb-2">Starter</h3>
                <p className="text-body text-text-secondary h-12">Find your biggest bottlenecks across a single team.</p>
              </div>
              <div className="mb-8">
                <span className="text-4xl font-bold text-text-primary">$499</span>
                <span className="text-text-secondary">/month</span>
              </div>
              <div className="flex-grow">
                <ul className="space-y-4 mb-8">
                  <li className="flex items-start gap-3 text-sm text-text-secondary">
                    <CheckCircle2 className="w-5 h-5 text-accent-blue shrink-0" /> Up to 25 users
                  </li>
                  <li className="flex items-start gap-3 text-sm text-text-secondary">
                    <CheckCircle2 className="w-5 h-5 text-accent-blue shrink-0" /> 1 Active Diagnostic Instrument
                  </li>
                  <li className="flex items-start gap-3 text-sm text-text-secondary">
                    <CheckCircle2 className="w-5 h-5 text-accent-blue shrink-0" /> Basic Finding Reports
                  </li>
                  <li className="flex items-start gap-3 text-sm text-text-secondary">
                    <CheckCircle2 className="w-5 h-5 text-accent-blue shrink-0" /> Email Support
                  </li>
                </ul>
              </div>
              <Link to="/register" className="w-full block text-center px-6 py-3 bg-bg-secondary border border-border-strong rounded-md hover:bg-bg-tertiary transition-colors text-text-primary font-medium">
                Start Free Trial
              </Link>
            </div>

            {/* Growth */}
            <div className="bg-bg-primary border-2 border-accent-blue rounded-xl p-8 shadow-md flex flex-col relative transform md:-translate-y-4">
              <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-accent-blue text-text-inverse px-4 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
                Most Popular
              </div>
              <div className="mb-8 mt-2">
                <h3 className="text-2xl font-bold text-text-primary mb-2">Growth</h3>
                <p className="text-body text-text-secondary h-12">Improve operational efficiency across multiple departments.</p>
              </div>
              <div className="mb-8">
                <span className="text-4xl font-bold text-text-primary">$999</span>
                <span className="text-text-secondary">/month</span>
              </div>
              <div className="flex-grow">
                <ul className="space-y-4 mb-8">
                  <li className="flex items-start gap-3 text-sm text-text-secondary">
                    <CheckCircle2 className="w-5 h-5 text-accent-blue shrink-0" /> Up to 100 users
                  </li>
                  <li className="flex items-start gap-3 text-sm text-text-secondary">
                    <CheckCircle2 className="w-5 h-5 text-accent-blue shrink-0" /> Full Diagnostic Suite
                  </li>
                  <li className="flex items-start gap-3 text-sm text-text-secondary">
                    <CheckCircle2 className="w-5 h-5 text-accent-blue shrink-0" /> Advanced Impact Quantification
                  </li>
                  <li className="flex items-start gap-3 text-sm text-text-secondary">
                    <CheckCircle2 className="w-5 h-5 text-accent-blue shrink-0" /> Cross-team Bottleneck Mapping
                  </li>
                  <li className="flex items-start gap-3 text-sm text-text-secondary">
                    <CheckCircle2 className="w-5 h-5 text-accent-blue shrink-0" /> Priority Support
                  </li>
                </ul>
              </div>
              <Link to="/register" className="w-full block text-center px-6 py-3 bg-accent-blue rounded-md hover:bg-accent-blue/90 transition-colors text-text-inverse font-medium">
                Start Free Trial
              </Link>
            </div>

            {/* Scale */}
            <div className="bg-bg-primary border border-border-strong rounded-xl p-8 shadow-sm flex flex-col">
              <div className="mb-8">
                <h3 className="text-2xl font-bold text-text-primary mb-2">Scale</h3>
                <p className="text-body text-text-secondary h-12">Build operational clarity across global teams.</p>
              </div>
              <div className="mb-8">
                <span className="text-4xl font-bold text-text-primary">Custom</span>
              </div>
              <div className="flex-grow">
                <ul className="space-y-4 mb-8">
                  <li className="flex items-start gap-3 text-sm text-text-secondary">
                    <CheckCircle2 className="w-5 h-5 text-text-primary shrink-0" /> Unlimited users
                  </li>
                  <li className="flex items-start gap-3 text-sm text-text-secondary">
                    <CheckCircle2 className="w-5 h-5 text-text-primary shrink-0" /> Custom Diagnostic Instruments
                  </li>
                  <li className="flex items-start gap-3 text-sm text-text-secondary">
                    <CheckCircle2 className="w-5 h-5 text-text-primary shrink-0" /> API Access & Integration
                  </li>
                  <li className="flex items-start gap-3 text-sm text-text-secondary">
                    <CheckCircle2 className="w-5 h-5 text-text-primary shrink-0" /> Dedicated Success Manager
                  </li>
                  <li className="flex items-start gap-3 text-sm text-text-secondary">
                    <CheckCircle2 className="w-5 h-5 text-text-primary shrink-0" /> Custom SLA
                  </li>
                </ul>
              </div>
              <Link to="/contact" className="w-full block text-center px-6 py-3 bg-bg-secondary border border-border-strong rounded-md hover:bg-bg-tertiary transition-colors text-text-primary font-medium">
                Contact Sales
              </Link>
            </div>

          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-24 bg-bg-primary text-center px-6 lg:px-8">
        <h2 className="text-h2 text-text-primary mb-6">Need more details?</h2>
        <p className="text-body text-text-secondary mb-8">Check out our full documentation or reach out to our team.</p>
        <div className="flex justify-center gap-4">
          <Link to="/resources/faq" className="text-accent-blue font-medium hover:underline">Read the FAQ</Link>
          <span className="text-text-secondary">or</span>
          <Link to="/contact" className="text-accent-blue font-medium hover:underline">Contact Us</Link>
        </div>
      </section>

    </div>
  );
}
