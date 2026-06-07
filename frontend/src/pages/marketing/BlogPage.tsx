import { Link } from 'react-router-dom';
import { SeoHead } from '../../components/geo/SeoHead';

export default function BlogPage() {
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
        "name": "Blog",
        "item": "https://tarkax.com/blog"
      }
    ]
  };

  const articleSchema = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Research & Insights on Operational Execution",
    "author": {
      "@type": "Organization",
      "name": "TarkaX"
    },
    "publisher": {
      "@type": "Organization",
      "name": "TarkaX",
      "logo": {
        "@type": "ImageObject",
        "url": "https://tarkax.com/logo.png"
      }
    }
  };

  return (
    <div className="bg-bg-primary">
      <SeoHead
        title="Research & Insights | TarkaX"
        description="Observations on operational execution, failure intelligence, and organizational diagnostics from TarkaX."
        canonical="https://tarkax.com/blog"
        schema={[breadcrumbSchema, articleSchema]}
      />
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
               <Link to="/contact?interest=Research" className="border border-border-light rounded-lg overflow-hidden flex flex-col cursor-pointer shadow-subtle hover:shadow-card transition-shadow duration-300">
                  <div className="h-48 bg-bg-secondary border-b border-border-light flex items-center justify-center p-6 text-center">
                     <span className="text-text-primary font-medium tracking-wide text-h3">The AI Initiative Was Approved. Adoption Never Happened.</span>
                  </div>
                  <div className="p-space-md flex-grow flex flex-col bg-bg-primary">
                     <div className="text-label text-text-secondary mb-space-xs">Failure Intelligence</div>
                     <h3 className="text-h3 text-text-primary mb-space-sm">
                        The AI Initiative Was Approved. Adoption Never Happened.
                     </h3>
                     <p className="text-body text-text-secondary line-clamp-3 mb-space-md">
                        Investigating the gap between executive mandate and operational reality. Why top-down AI initiatives stall without structural workflow integration.
                     </p>
                     <div className="mt-auto text-body font-medium text-accent-blue">Contact Us for Full Analysis →</div>
                  </div>
               </Link>

               {/* Supporting */}
               <div className="flex flex-col gap-space-lg">
                 <Link to="/contact?interest=Research" className="flex gap-space-sm cursor-pointer group">
                    <div className="w-32 h-24 bg-bg-secondary border border-border-light rounded-md shrink-0 shadow-subtle flex items-center justify-center text-center p-2">
                      <span className="text-text-secondary text-[10px] uppercase font-mono">Article</span>
                    </div>
                    <div>
                       <div className="text-label text-text-secondary mb-space-xs">Governance</div>
                       <h4 className="text-body font-medium text-text-primary mb-space-xs group-hover:text-accent-blue transition-colors">
                          The Governance Gap Nobody Owned
                       </h4>
                       <p className="text-body text-text-secondary line-clamp-2">
                          When policies are written but never integrated into the actual workflow, compliance becomes theater. How to spot unowned governance gaps.
                       </p>
                    </div>
                 </Link>
                 <Link to="/sample-report" className="flex gap-space-sm cursor-pointer group">
                    <div className="w-32 h-24 bg-bg-secondary border border-border-light rounded-md shrink-0 shadow-subtle flex items-center justify-center text-center p-2">
                      <span className="text-text-secondary text-[10px] uppercase font-mono">Report</span>
                    </div>
                    <div>
                       <div className="text-label text-text-secondary mb-space-xs">Adoption Risk</div>
                       <h4 className="text-body font-medium text-text-primary mb-space-xs group-hover:text-accent-blue transition-colors">
                          When AI Readiness Scores Hide Operational Risk
                       </h4>
                       <p className="text-body text-text-secondary line-clamp-2">
                          Why traditional sentiment-based assessments fail to measure true operational readiness and often create a false sense of security. View Sample Report.
                       </p>
                    </div>
                 </Link>
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
               <Link to="/contact?interest=Research" className="border border-border-light rounded-lg overflow-hidden flex flex-col cursor-pointer shadow-subtle hover:shadow-card transition-shadow duration-300">
                  <div className="p-space-md flex-grow flex flex-col bg-bg-primary">
                     <div className="text-label text-text-secondary mb-space-xs">Diagnostic Frameworks</div>
                     <h3 className="text-h3 text-text-primary mb-space-sm">
                        The Bottleneck Wasn't the Process. It Was Visibility.
                     </h3>
                     <p className="text-body text-text-secondary line-clamp-3 mb-space-md">
                        Why optimizing a documented process map rarely fixes execution issues when the true workflow happens in undocumented shadow systems.
                     </p>
                     <div className="mt-auto text-body font-medium text-accent-blue">Contact Us for Full Analysis →</div>
                  </div>
               </Link>

               <div className="flex flex-col gap-space-lg">
                 <Link to="/contact?interest=Research" className="flex gap-space-sm cursor-pointer group">
                    <div>
                       <div className="text-label text-text-secondary mb-space-xs">Workflow Health</div>
                       <h4 className="text-body font-medium text-text-primary mb-space-xs group-hover:text-accent-blue transition-colors">
                          How Workflow Weaknesses Compound Over Time
                       </h4>
                       <p className="text-body text-text-secondary line-clamp-2">
                          Small frictions in daily operations don't scale linearly; they compound. Exploring the math behind operational drag.
                       </p>
                    </div>
                 </Link>
                 <Link to="/sample-report" className="flex gap-space-sm cursor-pointer group">
                    <div>
                       <div className="text-label text-text-secondary mb-space-xs">Assessment Flaws</div>
                       <h4 className="text-body font-medium text-text-primary mb-space-xs group-hover:text-accent-blue transition-colors">
                          What Traditional Assessments Fail to Measure
                       </h4>
                       <p className="text-body text-text-secondary line-clamp-2">
                          The danger of relying on "how do you feel about this tool" surveys over behavioral diagnostics. View Sample Report.
                       </p>
                    </div>
                 </Link>
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
               <Link to="/contact?interest=Research" className="border border-border-light rounded-lg overflow-hidden flex flex-col cursor-pointer shadow-subtle hover:shadow-card transition-shadow duration-300">
                  <div className="p-space-md flex-grow flex flex-col bg-bg-primary">
                     <div className="text-label text-text-secondary mb-space-xs">Advisory</div>
                     <h3 className="text-h3 text-text-primary mb-space-sm">
                        Turning Diagnostics Into Advisory Services
                     </h3>
                     <p className="text-body text-text-secondary line-clamp-3 mb-space-md">
                        How forward-thinking consulting firms are using operational intelligence platforms to transition from report-writers to strategic execution partners.
                     </p>
                     <div className="mt-auto text-body font-medium text-accent-blue pt-space-sm">Contact Us →</div>
                  </div>
               </Link>
               <Link to="/contact?interest=Methodology" className="border border-border-light rounded-lg overflow-hidden flex flex-col cursor-pointer shadow-subtle hover:shadow-card transition-shadow duration-300">
                  <div className="p-space-md flex-grow flex flex-col bg-bg-primary">
                     <div className="text-label text-text-secondary mb-space-xs">Methodology</div>
                     <h3 className="text-h3 text-text-primary mb-space-sm">
                        Building Repeatable Assessment Frameworks
                     </h3>
                     <p className="text-body text-text-secondary line-clamp-3 mb-space-md">
                        The architectural requirements for scaling a diagnostic practice across a diverse client portfolio without sacrificing depth.
                     </p>
                     <div className="mt-auto text-body font-medium text-accent-blue pt-space-sm">Contact Us →</div>
                  </div>
               </Link>
               <Link to="/sample-report" className="border border-border-light rounded-lg overflow-hidden flex flex-col cursor-pointer shadow-subtle hover:shadow-card transition-shadow duration-300">
                  <div className="p-space-md flex-grow flex flex-col bg-bg-primary">
                     <div className="text-label text-text-secondary mb-space-xs">Client Delivery</div>
                     <h3 className="text-h3 text-text-primary mb-space-sm">
                        Presenting AI Maturity Findings to Clients
                     </h3>
                     <p className="text-body text-text-secondary line-clamp-3 mb-space-md">
                        Structuring uncomfortable truths. How to deliver structural failure intelligence in a way that drives action rather than defensiveness.
                     </p>
                     <div className="mt-auto text-body font-medium text-accent-blue pt-space-sm">View Sample Report →</div>
                  </div>
               </Link>
            </div>
          </div>

        </div>
      </section>
    </div>
  );
}