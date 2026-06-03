import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { SeoHead } from '../../components/geo/SeoHead';
import { DefinitionBlock } from '../../components/geo/DefinitionBlock';

export default function AboutPage() {
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
        "name": "About",
        "item": "https://tarkax.com/about"
      }
    ]
  };

  return (
    <div className="bg-bg-primary">
      <SeoHead
        title="About TarkaX | Operational Intelligence Platform"
        description="Learn about TarkaX, an Operational Intelligence platform built to diagnose structural weaknesses, AI readiness gaps, and operational friction."
        canonical="https://tarkax.com/about"
        schema={[breadcrumbSchema]}
      />
      {/* Header */}
      <section className="py-[120px] border-b border-border-light bg-bg-secondary animate-fade-up">
        <div className="max-w-4xl mx-auto px-6 lg:px-8 text-center">
          <h1 className="text-h1 text-text-primary mb-space-sm">
            About TarkaX
          </h1>
          <p className="text-h3 font-normal text-text-secondary">
            Building the intelligence layer for organizational execution.
          </p>

          <div className="mt-8 text-left">
            <DefinitionBlock
              question="What is the mission of TarkaX?"
              answer="TarkaX exists to expose structural organizational weaknesses before they cause critical failures. We build diagnostic systems that translate operational noise into clear, evidence-based intelligence for leaders and consultants."
            />
          </div>
        </div>
      </section>

      {/* Content */}
      <section className="py-[80px] bg-bg-primary">
        <div className="max-w-3xl mx-auto px-6 lg:px-8 space-y-[80px]">

          {/* Why TarkaX Exists */}
          <div>
            <h2 className="text-h2 text-text-primary mb-space-md">Why TarkaX Exists</h2>
            <div className="text-body text-text-secondary space-y-space-sm">
              <p>
                Organizations rarely fail overnight. They fail slowly, through compounding inefficiencies, misaligned workflows, and governance blind spots that are visible long before they become critical. Yet, most organizations lack the mechanisms to observe these early signals.
              </p>
              <p>
                TarkaX was built to identify these structural realities. By focusing on evidence and operational patterns rather than subjective sentiment, we provide leadership with the clarity required to make structural interventions.
              </p>
            </div>
          </div>

          {/* The Category Perspective */}
          <div>
            <h2 className="text-h2 text-text-primary mb-space-md">Methodology: The TarkaX Approach</h2>
            <div className="text-body text-text-secondary space-y-space-sm mb-space-lg">
              <p>
                We operate on the methodology of Failure Intelligence—the discipline of studying how and why operations break down, and engineering systems to detect those patterns before they manifest as business failure.
              </p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse border border-border-light bg-bg-primary rounded-lg shadow-sm">
                <thead>
                  <tr className="bg-bg-secondary border-b border-border-light">
                    <th className="py-4 px-6 text-label text-text-secondary font-medium w-1/2">Traditional Approach</th>
                    <th className="py-4 px-6 text-label text-text-secondary font-medium w-1/2">TarkaX Methodology</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border-light text-body text-text-primary">
                  <tr>
                    <td className="py-4 px-6 text-text-secondary">Measures stated sentiment (e.g., surveys).</td>
                    <td className="py-4 px-6 font-medium">Evaluates structural reality through behavioral evidence.</td>
                  </tr>
                  <tr>
                    <td className="py-4 px-6 text-text-secondary">Focuses on isolated "process mapping" and theory.</td>
                    <td className="py-4 px-6 font-medium">Identifies friction, workarounds, and "shadow" processes.</td>
                  </tr>
                  <tr>
                    <td className="py-4 px-6 text-text-secondary">Generates generic, static scores.</td>
                    <td className="py-4 px-6 font-medium">Delivers diagnostic insights mapped to actionable decisions.</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="mt-space-md text-sm">
              <Link to="#" className="text-accent-blue font-medium hover:underline inline-flex items-center gap-1">
                Read our full Methodology <span className="text-[10px] bg-bg-secondary border border-border-light text-text-secondary px-1.5 py-0.5 rounded uppercase tracking-wider font-mono ml-1">Coming Soon</span>
              </Link>
            </div>
          </div>

          {/* The Builder */}
          <div>
            <h2 className="text-h2 text-text-primary mb-space-md">The Builder</h2>
            <div className="text-body text-text-secondary space-y-space-sm">
              <p>
                Work across business analysis, operational research, and AI adoption initiatives revealed a recurring pattern: organizations often struggled to identify early signals of operational weakness.
              </p>
              <p>
                Despite having the data, the intelligence required to interpret that data into diagnostic insights was missing. TarkaX was developed to bridge this gap, translating operational noise into clear, actionable intelligence.
              </p>
            </div>
          </div>

          {/* What Comes Next */}
          <div className="p-space-lg bg-bg-secondary border border-border-light rounded-lg shadow-subtle mb-space-xl">
            <h2 className="text-h3 text-text-primary mb-space-sm">What Comes Next</h2>
            <p className="text-body text-text-secondary">
              Our vision is to move from point-in-time assessments toward continuous operational intelligence. We are building the foundational diagnostics today to support the automated, real-time organizational observability systems of tomorrow.
            </p>
          </div>

          <div className="border-t border-border-light pt-space-lg">
            <h3 className="text-h3 text-text-primary mb-space-sm">Explore TarkaX Capabilities</h3>
            <div className="flex flex-wrap gap-4">
              <Link to="/ai-audit" className="text-accent-blue font-medium hover:underline flex items-center gap-1">
                AI Audit <ArrowRight className="w-4 h-4" />
              </Link>
              <Link to="/workflow-diagnostic" className="text-accent-blue font-medium hover:underline flex items-center gap-1">
                Workflow Diagnostic <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-[120px] bg-bg-dark text-text-inverse text-center">
        <div className="max-w-3xl mx-auto px-6 lg:px-8">
          <h2 className="text-h2 tracking-tight mb-space-lg">
            Evaluate your operational reality.
          </h2>
          <Link
            to="/contact"
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