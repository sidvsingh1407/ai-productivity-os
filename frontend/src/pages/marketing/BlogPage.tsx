import { Link } from 'react-router-dom';

export default function BlogPage() {
  return (
    <div className="bg-background">
      {/* Header */}
      <section className="pt-24 pb-16 bg-gray-50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <h1 className="text-4xl md:text-5xl font-light text-foreground tracking-tight mb-6">
            Research & Insights
          </h1>
          <p className="text-xl text-gray-600 font-light max-w-2xl leading-relaxed">
            Observations on operational execution, failure intelligence, and organizational diagnostics.
          </p>
        </div>
      </section>

      {/* Pillars */}
      <section className="py-20 bg-background">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 space-y-24">

          {/* Pillar 1: AI Failure Intelligence */}
          <div>
            <div className="mb-10 border-b border-gray-200 pb-4">
               <h2 className="text-2xl font-light text-foreground tracking-tight">AI Failure Intelligence</h2>
               <p className="text-gray-500 font-light mt-2">Analysis of real-world adoption failures and structural barriers to AI integration.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
               {/* Featured */}
               <div className="border border-gray-200 rounded-xl overflow-hidden flex flex-col cursor-pointer hover:shadow-md transition-shadow">
                  <div className="h-48 bg-gray-100 border-b border-gray-200 flex items-center justify-center">
                     <span className="text-gray-400 font-medium tracking-widest text-sm uppercase">Research Report</span>
                  </div>
                  <div className="p-6 flex-grow flex flex-col">
                     <div className="text-xs text-gray-500 mb-3">Failure Intelligence</div>
                     <h3 className="text-xl font-medium text-foreground mb-3 leading-snug">
                        The AI Program Was Approved. Adoption Never Happened.
                     </h3>
                     <p className="text-gray-600 font-light text-sm line-clamp-3 mb-4">
                        Investigating the gap between executive mandate and operational reality. Why top-down AI initiatives stall without structural workflow integration.
                     </p>
                     <div className="mt-auto text-sm font-medium text-foreground">Read Analysis →</div>
                  </div>
               </div>

               {/* Supporting */}
               <div className="flex flex-col gap-8">
                 <div className="flex gap-6 cursor-pointer group">
                    <div className="w-32 h-24 bg-gray-100 border border-gray-200 rounded-lg shrink-0"></div>
                    <div>
                       <div className="text-xs text-gray-500 mb-1">Case Study</div>
                       <h4 className="text-base font-medium text-foreground mb-2 group-hover:text-gray-600 transition-colors">
                          Governance Blind Spots in Shadow AI Deployment
                       </h4>
                       <p className="text-gray-600 font-light text-sm line-clamp-2">
                          When employees bypass formal procurement to use unvetted models, the resulting risk surface is often unmapped.
                       </p>
                    </div>
                 </div>
                 <div className="flex gap-6 cursor-pointer group">
                    <div className="w-32 h-24 bg-gray-100 border border-gray-200 rounded-lg shrink-0"></div>
                    <div>
                       <div className="text-xs text-gray-500 mb-1">Adoption Risk</div>
                       <h4 className="text-base font-medium text-foreground mb-2 group-hover:text-gray-600 transition-colors">
                          The False Proxy of License Activation Rates
                       </h4>
                       <p className="text-gray-600 font-light text-sm line-clamp-2">
                          Why counting logged-in users fails to measure true operational integration and value creation.
                       </p>
                    </div>
                 </div>
               </div>
            </div>
          </div>

          {/* Pillar 2: Operational Diagnostics */}
          <div>
            <div className="mb-10 border-b border-gray-200 pb-4">
               <h2 className="text-2xl font-light text-foreground tracking-tight">Operational Diagnostics</h2>
               <p className="text-gray-500 font-light mt-2">Methodologies for identifying and measuring structural weaknesses in workflows.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
               <div className="border border-gray-200 rounded-xl overflow-hidden flex flex-col cursor-pointer hover:shadow-md transition-shadow">
                  <div className="p-6 flex-grow flex flex-col">
                     <div className="text-xs text-gray-500 mb-3">Diagnostic Frameworks</div>
                     <h3 className="text-xl font-medium text-foreground mb-3 leading-snug">
                        Measuring the Cost of Institutional Workarounds
                     </h3>
                     <p className="text-gray-600 font-light text-sm line-clamp-3 mb-4">
                        When process breaks down, employees create hidden systems. How to identify and quantify the impact of unmapped workflows.
                     </p>
                     <div className="mt-auto text-sm font-medium text-foreground">Read Analysis →</div>
                  </div>
               </div>
               <div className="border border-gray-200 rounded-xl overflow-hidden flex flex-col cursor-pointer hover:shadow-md transition-shadow">
                  <div className="p-6 flex-grow flex flex-col">
                     <div className="text-xs text-gray-500 mb-3">Process Evaluation</div>
                     <h3 className="text-xl font-medium text-foreground mb-3 leading-snug">
                        Identifying Structural Bottlenecks in Data Handoffs
                     </h3>
                     <p className="text-gray-600 font-light text-sm line-clamp-3 mb-4">
                        A framework for evaluating the exact points where operational execution consistently slows due to structural misalignment.
                     </p>
                     <div className="mt-auto text-sm font-medium text-foreground">Read Analysis →</div>
                  </div>
               </div>
            </div>
          </div>

          {/* Pillar 3: Consulting Insights */}
          <div>
            <div className="mb-10 border-b border-gray-200 pb-4">
               <h2 className="text-2xl font-light text-foreground tracking-tight">Consulting Insights</h2>
               <p className="text-gray-500 font-light mt-2">How advisors can operationalize diagnostics to drive client interventions.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
               <div className="border border-gray-200 rounded-xl overflow-hidden flex flex-col cursor-pointer hover:shadow-md transition-shadow">
                  <div className="p-6 flex-grow flex flex-col">
                     <h3 className="text-lg font-medium text-foreground mb-3 leading-snug">
                        Moving Clients from Subjective to Quantitative Baselines
                     </h3>
                     <div className="mt-auto text-sm font-medium text-foreground pt-4">Read Article →</div>
                  </div>
               </div>
               <div className="border border-gray-200 rounded-xl overflow-hidden flex flex-col cursor-pointer hover:shadow-md transition-shadow">
                  <div className="p-6 flex-grow flex flex-col">
                     <h3 className="text-lg font-medium text-foreground mb-3 leading-snug">
                        Standardizing Failure Diagnostics Across Portfolios
                     </h3>
                     <div className="mt-auto text-sm font-medium text-foreground pt-4">Read Article →</div>
                  </div>
               </div>
               <div className="border border-gray-200 rounded-xl overflow-hidden flex flex-col cursor-pointer hover:shadow-md transition-shadow">
                  <div className="p-6 flex-grow flex flex-col">
                     <h3 className="text-lg font-medium text-foreground mb-3 leading-snug">
                        Using Evidence to Justify Structural Interventions
                     </h3>
                     <div className="mt-auto text-sm font-medium text-foreground pt-4">Read Article →</div>
                  </div>
               </div>
            </div>
          </div>

        </div>
      </section>
    </div>
  );
}