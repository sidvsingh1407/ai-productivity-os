import { Link } from 'react-router-dom';
import { ArrowRight, CheckCircle2 } from 'lucide-react';

export default function AiAuditPage() {
  return (
    <div className="bg-background">
      {/* Header */}
      <section className="pt-24 pb-16 bg-gray-50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="inline-block px-3 py-1 bg-white border border-gray-200 text-gray-600 text-xs font-medium rounded-full mb-6 uppercase tracking-wider">
            Flagship Module
          </div>
          <h1 className="text-4xl md:text-5xl font-light text-foreground tracking-tight max-w-3xl mb-6">
            AI Audit
          </h1>
          <p className="text-xl text-gray-600 font-light max-w-2xl leading-relaxed">
            Establish a quantitative baseline for organizational AI readiness.
          </p>
        </div>
      </section>

      {/* Problem */}
      <section className="py-20 bg-background border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 grid grid-cols-1 md:grid-cols-3 gap-12">
          <div className="col-span-1">
            <h2 className="text-2xl font-light text-foreground tracking-tight">The Problem</h2>
          </div>
          <div className="col-span-2">
            <p className="text-lg text-gray-600 font-light leading-relaxed mb-6">
              Organizations frequently deploy AI tools without assessing underlying structural readiness. This leads to fragmented adoption, unmanaged risk, and an inability to measure return on investment.
            </p>
            <p className="text-lg text-gray-600 font-light leading-relaxed">
              The AI Audit evaluates the organization's actual capacity to integrate and govern artificial intelligence, moving beyond surface-level tool counts to structural truths.
            </p>
          </div>
        </div>
      </section>

      {/* What It Measures & Dimensions */}
      <section className="py-20 bg-gray-50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <h2 className="text-3xl font-light text-foreground tracking-tight mb-12 text-center">
            Assessment Dimensions
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
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
              <div key={i} className="bg-white p-8 rounded-xl border border-gray-200 shadow-sm">
                <h3 className="text-xl font-medium text-foreground mb-4">{dim.title}</h3>
                <p className="text-gray-600 font-light">{dim.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Sample Outputs */}
      <section className="py-20 bg-background border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-3xl font-light text-foreground tracking-tight mb-6">
                Sample Outputs
              </h2>
              <ul className="space-y-6">
                <li className="flex items-start gap-4">
                  <CheckCircle2 className="w-6 h-6 text-gray-400 shrink-0 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-foreground">Maturity Assessment</h4>
                    <p className="text-gray-600 font-light mt-1">Quantitative scoring across all five dimensions to establish a clear baseline.</p>
                  </div>
                </li>
                <li className="flex items-start gap-4">
                  <CheckCircle2 className="w-6 h-6 text-gray-400 shrink-0 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-foreground">Governance Insights</h4>
                    <p className="text-gray-600 font-light mt-1">Identification of critical blind spots in policy, data access, and compliance.</p>
                  </div>
                </li>
                <li className="flex items-start gap-4">
                  <CheckCircle2 className="w-6 h-6 text-gray-400 shrink-0 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-foreground">Actionable Recommendations</h4>
                    <p className="text-gray-600 font-light mt-1">Prioritized interventions designed to mitigate risk and improve integration capability.</p>
                  </div>
                </li>
              </ul>
            </div>
            <div className="bg-gray-50 p-8 rounded-xl border border-gray-200 h-full flex flex-col justify-center">
               <div className="space-y-4">
                 <div className="flex justify-between items-center text-sm mb-1">
                   <span className="font-medium text-foreground">Governance Maturity</span>
                   <span className="text-gray-500">L2 - Reactive</span>
                 </div>
                 <div className="w-full bg-gray-200 rounded-full h-2">
                   <div className="bg-foreground h-2 rounded-full" style={{ width: '40%' }}></div>
                 </div>
                 <div className="mt-6 pt-6 border-t border-gray-200">
                    <p className="text-sm font-medium text-foreground mb-2">Key Finding:</p>
                    <p className="text-sm text-gray-600 font-light">Shadow IT adoption has outpaced policy creation. Data governance frameworks must be updated before further integration.</p>
                 </div>
               </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 bg-foreground text-background text-center">
        <div className="max-w-3xl mx-auto px-6 lg:px-8">
          <h2 className="text-3xl font-light tracking-tight mb-8">
            Baseline your organization's readiness.
          </h2>
          <Link
            to="/contact?interest=AI+Audit"
            className="inline-flex items-center justify-center px-8 py-4 bg-background text-foreground font-medium rounded-lg hover:bg-gray-100 transition-all gap-2"
          >
            Request a Demo
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>
    </div>
  );
}