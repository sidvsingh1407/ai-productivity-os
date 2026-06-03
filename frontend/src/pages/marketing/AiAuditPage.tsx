import { Link } from 'react-router-dom';
import { ArrowRight, CheckCircle2 } from 'lucide-react';

export default function AiAuditPage() {
  return (
    <div className="bg-bg-primary">
      {/* Header */}
      <section className="pt-[120px] pb-[80px] bg-bg-secondary border-b border-border-light animate-fade-up">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="inline-block px-3 py-1 bg-bg-primary border border-border-light text-text-secondary text-label rounded-full mb-space-md">
            Flagship Module
          </div>
          <h1 className="text-h1 text-text-primary max-w-3xl mb-space-sm">
            AI Audit
          </h1>
          <p className="text-h3 font-normal text-text-secondary max-w-2xl">
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
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-space-lg">
            {[
              {
                title: "Awareness",
                desc: "Does the organization understand what is possible and what is required?"
              },
              {
                title: "Adoption",
                desc: "How deeply are existing tools integrated into daily operations?"
              },
              {
                title: "Integration",
                desc: "Are systems technically and structurally aligned to support AI capabilities?"
              },
              {
                title: "Governance",
                desc: "Are policies, risks, and data access properly controlled and monitored?"
              },
              {
                title: "ROI",
                desc: "Is there a mechanism to measure the operational value being created?"
              }
            ].map((dim, i) => (
              <div key={i} className="bg-bg-primary p-space-md rounded-lg border border-border-light shadow-subtle hover:shadow-card transition-shadow duration-300">
                <h3 className="text-h3 text-text-primary mb-space-xs">{dim.title}</h3>
                <p className="text-body text-text-secondary">{dim.desc}</p>
              </div>
            ))}
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
        </div>
      </section>

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