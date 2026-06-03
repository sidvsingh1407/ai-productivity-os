import { Link } from 'react-router-dom';

export default function BlogPage() {
  return (
    <div className="bg-bg-primary">
      {/* Header */}
      <section className="pt-[120px] pb-[80px] bg-bg-secondary border-b border-border-light animate-fade-up">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <h1 className="text-h1 text-text-primary mb-space-sm">
            Research & Insights
          </h1>
          <p className="text-h3 font-normal text-text-secondary max-w-2xl">
            Observations on operational execution, failure intelligence, and organizational diagnostics.
          </p>
        </div>
      </section>

      {/* Pillars */}
      <section className="py-[80px] bg-bg-primary">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 space-y-[80px]">

          {/* Pillar 1: AI Failure Intelligence */}
          <div>
            <div className="mb-space-lg border-b border-border-strong pb-space-sm">
               <h2 className="text-h2 text-text-primary">AI Failure Intelligence</h2>
               <p className="text-body text-text-secondary mt-space-xs">Analysis of real-world adoption failures and structural barriers to AI integration.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-space-lg">
               {/* Featured */}
               <div className="border border-border-light rounded-lg overflow-hidden flex flex-col cursor-pointer shadow-subtle hover:shadow-card transition-shadow duration-300">
                  <div className="h-48 bg-bg-secondary border-b border-border-light flex items-center justify-center">
                     <span className="text-text-secondary font-medium tracking-widest text-label uppercase">Research Report</span>
                  </div>
                  <div className="p-space-md flex-grow flex flex-col bg-bg-primary">
                     <div className="text-label text-text-secondary mb-space-xs">Failure Intelligence</div>
                     <h3 className="text-h3 text-text-primary mb-space-sm">
                        The AI Program Was Approved. Adoption Never Happened.
                     </h3>
                     <p className="text-body text-text-secondary line-clamp-3 mb-space-md">
                        Investigating the gap between executive mandate and operational reality. Why top-down AI initiatives stall without structural workflow integration.
                     </p>
                     <div className="mt-auto text-body font-medium text-accent-blue">Read Analysis →</div>
                  </div>
               </div>

               {/* Supporting */}
               <div className="flex flex-col gap-space-lg">
                 <div className="flex gap-space-sm cursor-pointer group">
                    <div className="w-32 h-24 bg-bg-secondary border border-border-light rounded-md shrink-0 shadow-subtle"></div>
                    <div>
                       <div className="text-label text-text-secondary mb-space-xs">Case Study</div>
                       <h4 className="text-body font-medium text-text-primary mb-space-xs group-hover:text-accent-blue transition-colors">
                          Governance Blind Spots in Shadow AI Deployment
                       </h4>
                       <p className="text-body text-text-secondary line-clamp-2">
                          When employees bypass formal procurement to use unvetted models, the resulting risk surface is often unmapped.
                       </p>
                    </div>
                 </div>
                 <div className="flex gap-space-sm cursor-pointer group">
                    <div className="w-32 h-24 bg-bg-secondary border border-border-light rounded-md shrink-0 shadow-subtle"></div>
                    <div>
                       <div className="text-label text-text-secondary mb-space-xs">Adoption Risk</div>
                       <h4 className="text-body font-medium text-text-primary mb-space-xs group-hover:text-accent-blue transition-colors">
                          The False Proxy of License Activation Rates
                       </h4>
                       <p className="text-body text-text-secondary line-clamp-2">
                          Why counting logged-in users fails to measure true operational integration and value creation.
                       </p>
                    </div>
                 </div>
               </div>
            </div>
          </div>

          {/* Pillar 2: Operational Diagnostics */}
          <div>
            <div className="mb-space-lg border-b border-border-strong pb-space-sm">
               <h2 className="text-h2 text-text-primary">Operational Diagnostics</h2>
               <p className="text-body text-text-secondary mt-space-xs">Methodologies for identifying and measuring structural weaknesses in workflows.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-space-lg">
               <div className="border border-border-light rounded-lg overflow-hidden flex flex-col cursor-pointer shadow-subtle hover:shadow-card transition-shadow duration-300">
                  <div className="p-space-md flex-grow flex flex-col bg-bg-primary">
                     <div className="text-label text-text-secondary mb-space-xs">Diagnostic Frameworks</div>
                     <h3 className="text-h3 text-text-primary mb-space-sm">
                        Measuring the Cost of Institutional Workarounds
                     </h3>
                     <p className="text-body text-text-secondary line-clamp-3 mb-space-md">
                        When process breaks down, employees create hidden systems. How to identify and quantify the impact of unmapped workflows.
                     </p>
                     <div className="mt-auto text-body font-medium text-accent-blue">Read Analysis →</div>
                  </div>
               </div>
               <div className="border border-border-light rounded-lg overflow-hidden flex flex-col cursor-pointer shadow-subtle hover:shadow-card transition-shadow duration-300">
                  <div className="p-space-md flex-grow flex flex-col bg-bg-primary">
                     <div className="text-label text-text-secondary mb-space-xs">Process Evaluation</div>
                     <h3 className="text-h3 text-text-primary mb-space-sm">
                        Identifying Structural Bottlenecks in Data Handoffs
                     </h3>
                     <p className="text-body text-text-secondary line-clamp-3 mb-space-md">
                        A framework for evaluating the exact points where operational execution consistently slows due to structural misalignment.
                     </p>
                     <div className="mt-auto text-body font-medium text-accent-blue">Read Analysis →</div>
                  </div>
               </div>
            </div>
          </div>

          {/* Pillar 3: Consulting Insights */}
          <div>
            <div className="mb-space-lg border-b border-border-strong pb-space-sm">
               <h2 className="text-h2 text-text-primary">Consulting Insights</h2>
               <p className="text-body text-text-secondary mt-space-xs">How advisors can operationalize diagnostics to drive client interventions.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-space-lg">
               <div className="border border-border-light rounded-lg overflow-hidden flex flex-col cursor-pointer shadow-subtle hover:shadow-card transition-shadow duration-300">
                  <div className="p-space-md flex-grow flex flex-col bg-bg-primary">
                     <h3 className="text-h3 text-text-primary mb-space-sm">
                        Moving Clients from Subjective to Quantitative Baselines
                     </h3>
                     <div className="mt-auto text-body font-medium text-accent-blue pt-space-sm">Read Article →</div>
                  </div>
               </div>
               <div className="border border-border-light rounded-lg overflow-hidden flex flex-col cursor-pointer shadow-subtle hover:shadow-card transition-shadow duration-300">
                  <div className="p-space-md flex-grow flex flex-col bg-bg-primary">
                     <h3 className="text-h3 text-text-primary mb-space-sm">
                        Standardizing Failure Diagnostics Across Portfolios
                     </h3>
                     <div className="mt-auto text-body font-medium text-accent-blue pt-space-sm">Read Article →</div>
                  </div>
               </div>
               <div className="border border-border-light rounded-lg overflow-hidden flex flex-col cursor-pointer shadow-subtle hover:shadow-card transition-shadow duration-300">
                  <div className="p-space-md flex-grow flex flex-col bg-bg-primary">
                     <h3 className="text-h3 text-text-primary mb-space-sm">
                        Using Evidence to Justify Structural Interventions
                     </h3>
                     <div className="mt-auto text-body font-medium text-accent-blue pt-space-sm">Read Article →</div>
                  </div>
               </div>
            </div>
          </div>

        </div>
      </section>
    </div>
  );
}