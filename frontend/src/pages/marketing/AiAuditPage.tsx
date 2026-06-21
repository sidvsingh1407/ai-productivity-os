import { Link } from 'react-router-dom';
import { ArrowRight, CheckCircle2 } from 'lucide-react';
import { SeoHead } from '../../components/geo/SeoHead';
import { DefinitionBlock } from '../../components/geo/DefinitionBlock';
import { FAQSection, generateFAQSchema } from '../../components/geo/FAQSection';

export default function AiAuditPage() {
  const faqItems = [
    {
      question: "What does an AI Audit measure?",
      answer: "An AI Audit measures an organization's structural readiness to adopt and scale artificial intelligence. It evaluates governance frameworks, knowledge silos, technology infrastructure, and cultural alignment to identify where AI initiatives are most likely to break down."
    },
    {
      question: "How is an AI Audit different from an IT assessment?",
      answer: "While IT assessments focus on infrastructure and security compliance, an AI Audit evaluates operational integration, business alignment, and Failure Intelligence. It measures whether the organization can actually extract value from AI investments."
    },
    {
      question: "What is the typical output of an AI Audit?",
      answer: "The output is an actionable diagnostic report detailing maturity scores across key dimensions, identifying critical capability gaps, and providing prioritized operational interventions to mitigate adoption risk."
    }
  ];

  const breadcrumbSchema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://tarkax.com/"
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": "AI Audit",
        "item": "https://tarkax.com/ai-audit"
      }
    ]
  };

  const faqSchema = generateFAQSchema(faqItems);

  return (
    <div className="bg-bg-primary">
      <SeoHead
        title="AI Audit | TarkaX"
        description="Establish a quantitative baseline for organizational AI readiness. Evaluate governance, integration, and operational maturity with TarkaX's AI Audit."
        canonical="https://tarkax.com/ai-audit"
        schema={[breadcrumbSchema, faqSchema]}
      />
      {/* Header */}
      <section className="pt-[120px] pb-[80px] bg-bg-secondary border-b border-border-light animate-fade-up">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="inline-block px-3 py-1 bg-bg-primary border border-border-light text-text-secondary text-label rounded-full mb-space-md">
            Flagship Module
          </div>
          <h1 className="text-h1 text-text-primary max-w-3xl mb-space-sm">
            AI Audit
          </h1>

          <div className="mt-8 max-w-3xl w-full">
            <DefinitionBlock
              question="What is an AI Audit?"
              answer="An AI Audit is a diagnostic evaluation of an organization's structural readiness to adopt and scale artificial intelligence. It identifies governance gaps, operational misalignment, and execution risks before capital is deployed."
            />
          </div>

          <p className="mt-space-md text-h3 font-normal text-text-secondary max-w-2xl">
            Establish a quantitative baseline for organizational AI readiness.
          </p>
        </div>
      </section>

      {/* Problem */}
      <section className="py-[80px] bg-bg-primary border-b border-border-light">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 grid grid-cols-1 md:grid-cols-3 gap-space-xl">
          <div className="col-span-1">
            <h2 className="text-h2 text-text-primary">The Problem</h2>
          </div>
          <div className="col-span-2">
            <p className="text-body text-text-secondary mb-space-sm">
              Organizations frequently deploy AI tools without assessing underlying structural readiness. This leads to fragmented adoption, unmanaged risk, and an inability to measure return on investment.
            </p>
            <p className="text-body text-text-secondary">
              The AI Audit evaluates the organization's actual capacity to integrate and govern artificial intelligence, moving beyond surface-level tool counts to structural truths.
            </p>
          </div>
        </div>
      </section>

      {/* What It Measures & Dimensions */}
      <section className="py-[80px] bg-bg-secondary border-b border-border-light">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <h2 className="text-h2 text-text-primary mb-space-xl text-center">
            Assessment Dimensions
          </h2>
          <div className="overflow-x-auto max-w-5xl mx-auto">
            <table className="w-full text-left border-collapse border border-border-light bg-bg-primary rounded-lg shadow-sm">
              <thead>
                <tr className="bg-bg-secondary border-b border-border-light">
                  <th className="py-4 px-6 text-label text-text-secondary font-medium w-1/3">Dimension</th>
                  <th className="py-4 px-6 text-label text-text-secondary font-medium">Diagnostic Focus</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-light text-body text-text-primary">
                <tr>
                  <td className="py-4 px-6 font-medium">Awareness</td>
                  <td className="py-4 px-6 text-text-secondary">Does the organization understand what is possible and what is required operationally?</td>
                </tr>
                <tr>
                  <td className="py-4 px-6 font-medium">Adoption</td>
                  <td className="py-4 px-6 text-text-secondary">How deeply are existing tools integrated into daily operations versus sporadic usage?</td>
                </tr>
                <tr>
                  <td className="py-4 px-6 font-medium">Integration</td>
                  <td className="py-4 px-6 text-text-secondary">Are systems technically and structurally aligned to support advanced capabilities?</td>
                </tr>
                <tr>
                  <td className="py-4 px-6 font-medium">Governance</td>
                  <td className="py-4 px-6 text-text-secondary">Are policies, risks, and data access properly controlled and monitored?</td>
                </tr>
                <tr>
                  <td className="py-4 px-6 font-medium">Value Realization (ROI)</td>
                  <td className="py-4 px-6 text-text-secondary">Is there a mechanism to measure the operational value being created by the initiative?</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* Sample Outputs */}
      <section className="py-[80px] bg-bg-primary border-b border-border-light">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-space-xl items-center">
            <div>
              <h2 className="text-h2 text-text-primary mb-space-md">
                Sample Outputs
              </h2>
              <ul className="space-y-space-md">
                <li className="flex items-start gap-4">
                  <CheckCircle2 className="w-6 h-6 text-text-secondary shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-body font-medium text-text-primary">Maturity Assessment</h4>
                    <p className="text-body text-text-secondary mt-1">Quantitative scoring across all five dimensions to establish a clear baseline.</p>
                  </div>
                </li>
                <li className="flex items-start gap-4">
                  <CheckCircle2 className="w-6 h-6 text-text-secondary shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-body font-medium text-text-primary">Governance Insights</h4>
                    <p className="text-body text-text-secondary mt-1">Identification of critical blind spots in policy, data access, and compliance.</p>
                  </div>
                </li>
                <li className="flex items-start gap-4">
                  <CheckCircle2 className="w-6 h-6 text-text-secondary shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-body font-medium text-text-primary">Actionable Recommendations</h4>
                    <p className="text-body text-text-secondary mt-1">Prioritized interventions designed to mitigate risk and improve integration capability.</p>
                  </div>
                </li>
              </ul>
            </div>
            <div className="bg-bg-secondary p-space-lg rounded-lg border border-border-light h-full flex flex-col justify-center shadow-subtle">
               <div className="space-y-4">
                 <div className="flex justify-between items-center text-body mb-1">
                   <span className="font-medium text-text-primary">Governance Maturity</span>
                   <span className="text-data text-text-secondary">L2 - Reactive</span>
                 </div>
                 <div className="w-full bg-border-light rounded-full h-2">
                   <div className="bg-accent-blue h-2 rounded-full" style={{ width: '40%' }}></div>
                 </div>
                 <div className="mt-space-md pt-space-md border-t border-border-strong">
                    <p className="text-label text-text-primary mb-space-xs">Key Finding:</p>
                    <p className="text-body text-text-secondary">Shadow IT adoption has outpaced policy creation. Data governance frameworks must be updated before further integration.</p>
                 </div>
               </div>
            </div>
          </div>

          <div className="mt-space-xl border-t border-border-light pt-space-lg">
            <h3 className="text-h3 text-text-primary mb-space-sm">Explore Related Diagnostics</h3>
            <div className="flex gap-4 flex-wrap">
              <Link to="/example-findings" className="text-accent-blue font-medium hover:underline flex items-center gap-1">
                View Example Findings <ArrowRight className="w-4 h-4" />
              </Link>
              <Link to="/workflow-diagnostic" className="text-text-secondary font-medium hover:text-accent-blue flex items-center gap-1">
                See Where Workflows Break <ArrowRight className="w-4 h-4" />
              </Link>
              <Link to="/contact?interest=Forecasting Framework" className="text-text-secondary font-medium hover:text-accent-blue flex items-center gap-1">
                Forecasting Framework <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <FAQSection faqItems={faqItems} />

      {/* CTA */}
      <section className="py-[120px] bg-bg-dark text-text-inverse text-center">
        <div className="max-w-3xl mx-auto px-6 lg:px-8">
          <h2 className="text-h2 tracking-tight mb-space-lg">
            Baseline your organization's readiness.
          </h2>
          <Link
            to="/contact?interest=AI+Audit"
            className="inline-flex items-center justify-center px-8 py-4 bg-accent-blue text-text-inverse text-body font-medium rounded-md shadow-sm hover:bg-accent-blue/90 transition-colors gap-2"
          >
            Request a Demo
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  );
}