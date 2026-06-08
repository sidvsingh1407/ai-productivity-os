import { Link } from 'react-router-dom';
import { SeoHead } from '../../../components/geo/SeoHead';
import { ArrowRight, CheckCircle2, LayoutDashboard } from 'lucide-react';

interface SolutionTemplateProps {
  title: string;
  seoTitle: string;
  description: string;
  benefits: string[];
  howWeHelp: {
    step: string;
    detail: string;
  }[];
  productLensUrl: string;
  productLensLabel: string;
}

export function SolutionTemplate({
  title,
  seoTitle,
  description,
  benefits,
  howWeHelp,
  productLensUrl,
  productLensLabel
}: SolutionTemplateProps) {
  return (
    <div className="bg-bg-primary">
      <SeoHead
        title={`${seoTitle} | TarkaX`}
        description={description}
        canonical={`https://tarkax.com/solutions/${seoTitle.toLowerCase().replace(/ /g, '-')}`}
      />

      {/* Hero */}
      <section className="py-24 bg-bg-primary border-b border-border-strong">
        <div className="max-w-4xl mx-auto px-6 lg:px-8 text-center">
          <h1 className="text-display text-text-primary mb-6">{title}</h1>
          <p className="text-h3 font-normal text-text-secondary mb-12">{description}</p>
          <div className="flex justify-center gap-4">
            <Link
              to="/register"
              className="px-8 py-4 bg-accent-blue text-text-inverse text-body font-medium transition-colors hover:bg-accent-blue/90 inline-flex items-center justify-center rounded-md shadow-sm"
            >
              Start Free Analysis
            </Link>
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section className="py-24 bg-bg-secondary border-b border-border-strong">
        <div className="max-w-5xl mx-auto px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-h2 text-text-primary mb-4">The Impact of Clarity</h2>
            <p className="text-body text-text-secondary">What happens when you finally see the full picture.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {benefits.map((benefit, i) => (
              <div key={i} className="flex items-start gap-4 bg-bg-primary p-6 rounded-lg border border-border-light shadow-sm">
                <CheckCircle2 className="w-6 h-6 text-accent-blue shrink-0" />
                <p className="text-body text-text-secondary font-medium">{benefit}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How We Help */}
      <section className="py-24 bg-bg-primary border-b border-border-strong">
        <div className="max-w-4xl mx-auto px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-h2 text-text-primary mb-4">How TarkaX Delivers the Solution</h2>
            <p className="text-body text-text-secondary">Our process for turning operational chaos into structured intelligence.</p>
          </div>
          <div className="space-y-8">
            {howWeHelp.map((item, i) => (
              <div key={i} className="flex flex-col md:flex-row gap-6 items-start">
                <div className="w-12 h-12 bg-bg-secondary border border-border-strong rounded-full flex items-center justify-center font-bold text-text-primary shrink-0">
                  {i + 1}
                </div>
                <div>
                  <h3 className="text-xl font-bold text-text-primary mb-2">{item.step}</h3>
                  <p className="text-body text-text-secondary">{item.detail}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Product Lens CTA */}
      <section className="py-24 bg-bg-dark text-center text-text-inverse">
        <div className="max-w-3xl mx-auto px-6 lg:px-8">
          <LayoutDashboard className="w-12 h-12 text-accent-blue mx-auto mb-6" />
          <h2 className="text-display mb-6">Investigate This Area</h2>
          <p className="text-h3 font-normal text-text-inverse/80 mb-12">
            Use our specific diagnostic instruments to uncover the reality of your operations.
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
