import { Link } from 'react-router-dom';
import { ShieldAlert, ArrowRight } from 'lucide-react';
import { SeoHead } from '../../components/geo/SeoHead';
import { FAQSection, generateFAQSchema } from '../../components/geo/FAQSection';

export default function Home() {
  const faqItems = [
    {
      question: "What is Operational Intelligence?",
      answer: "Operational Intelligence is the practice of identifying operational risks, governance gaps, workflow weaknesses, and execution issues before they become larger organizational problems. It shifts the focus from backward-looking metrics to forward-looking operational realities."
    },
    {
      question: "What is Failure Intelligence?",
      answer: "Failure Intelligence is a systematic approach to identifying the specific, recurring patterns that cause initiatives, projects, or adoptions to fail within an organization. It focuses on structural barriers rather than individual performance."
    },
    {
      question: "What does an AI Audit measure?",
      answer: "An AI Audit measures an organization's structural readiness to adopt and scale artificial intelligence. It evaluates governance frameworks, knowledge silos, technology infrastructure, and cultural alignment to identify where AI initiatives are most likely to break down."
    },
    {
      question: "How is TarkaX different from traditional assessments?",
      answer: "Traditional assessments rely on point-in-time snapshots and stated sentiment to generate generic scores. TarkaX focuses on structural reality, using diagnostic frameworks to identify underlying failure patterns and provide actionable decision intelligence."
    }
  ];

  const organizationSchema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "TarkaX",
    "url": "https://tarkax.com",
    "logo": "https://tarkax.com/logo.png",
    "contactPoint": {
      "@type": "ContactPoint",
      "contactType": "Customer Service",
      "url": "https://tarkax.com/contact"
    }
  };

  const websiteSchema = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "TarkaX",
    "url": "https://tarkax.com"
  };

  const faqSchema = generateFAQSchema(faqItems);

  return (
    <div className="bg-bg-primary">
      <SeoHead
        title="TarkaX | Operational Intelligence Platform"
        description="TarkaX is an Operational Intelligence Platform built on Failure Intelligence principles. We help organizations identify AI adoption gaps, workflow weaknesses, and execution risks."
        canonical="https://tarkax.com/"
        schema={[organizationSchema, websiteSchema, faqSchema]}
      />
      {/* 1. Hero Section */}
      <section className="py-[120px] border-b border-border-strong bg-bg-primary">
        <div className="max-w-4xl mx-auto px-6 lg:px-8 text-center flex flex-col items-center">
          <h1 className="text-display text-text-primary mb-6">
            Operational Intelligence Platform
          </h1>
          <p className="text-h3 font-normal text-text-secondary max-w-3xl mb-12">
            TarkaX identifies structural failures, governance gaps, and execution risks before they become institutional problems.
          </p>
          <Link
            to="/contact"
            className="px-8 py-4 bg-text-primary text-text-inverse text-body font-medium transition-colors hover:bg-text-primary/90 flex items-center justify-center gap-2"
          >
            Request a Demo
          </Link>
        </div>
      </section>

      {/* 2. Problem Frame */}
      <section className="py-[80px] bg-bg-primary border-b border-border-strong">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-space-xl">
            <div>
              <h2 className="text-h2 text-text-primary mb-space-md">
                The Reality of Operational Execution
              </h2>
              <p className="text-body text-text-secondary">
                Most operational failures are visible before they become obvious. The signal often exists long before the problem is acknowledged by leadership.
              </p>
            </div>
            <div className="space-y-8">
              <div className="border-l-2 border-border-strong pl-6">
                <p className="text-body text-text-primary font-medium">Strategic initiatives fail not due to lack of vision, but due to structural misalignment in execution.</p>
              </div>
              <div className="border-l-2 border-border-strong pl-6">
                <p className="text-body text-text-primary font-medium">Traditional assessments measure stated sentiment. TarkaX measures operational reality.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 3. Methodology Section */}
      <section className="py-[80px] bg-bg-secondary border-b border-border-strong">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <h2 className="text-h2 text-text-primary mb-12 text-center">Diagnostic Methodology</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 bg-bg-primary border border-border-strong">
            <div className="p-8 border-b md:border-b-0 md:border-r border-border-strong">
              <div className="text-label text-text-secondary mb-4">Phase 01</div>
              <h3 className="text-h3 text-text-primary mb-4">Assess</h3>
              <p className="text-body text-text-secondary">
                Gather structural evidence across the organization using targeted diagnostic instruments designed to bypass perception bias.
              </p>
            </div>
            <div className="p-8 border-b md:border-b-0 md:border-r border-border-strong">
              <div className="text-label text-text-secondary mb-4">Phase 02</div>
              <h3 className="text-h3 text-text-primary mb-4">Diagnose</h3>
              <p className="text-body text-text-secondary">
                Identify recurring failure patterns, map capability gaps, and establish a quantitative baseline for organizational reality.
              </p>
            </div>
            <div className="p-8">
              <div className="text-label text-text-secondary mb-4">Phase 03</div>
              <h3 className="text-h3 text-text-primary mb-4">Improve</h3>
              <p className="text-body text-text-secondary">
                Deploy precise, targeted interventions based on diagnostic evidence to resolve structural blockers and execution risks.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 4. AI Maturity Score Preview */}
      <section className="py-[120px] bg-bg-primary border-b border-border-strong">
        <div className="max-w-5xl mx-auto px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-h2 text-text-primary mb-4">Consulting-Grade Output</h2>
            <p className="text-body text-text-secondary">Our assessments generate executive intelligence, not generic dashboard widgets.</p>
          </div>

          <div className="border border-border-strong bg-bg-primary p-8 md:p-12 shadow-sm">
            <div className="border-b border-border-strong pb-6 mb-8 flex justify-between items-end">
              <div>
                <h3 className="text-h2 font-medium text-text-primary">AI Readiness Diagnostic</h3>
                <p className="text-body text-text-secondary mt-1">Executive Summary</p>
              </div>
              <div className="text-right">
                <div className="text-data text-text-secondary">CONFIDENTIAL</div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
              <div className="col-span-1">
                <div className="text-label text-text-secondary mb-2">Overall AI Maturity Score</div>
                <div className="flex items-baseline gap-2 mb-4">
                  <span className="text-[72px] font-bold leading-none font-mono text-text-primary">72</span>
                  <span className="text-h3 font-mono text-text-secondary">/ 100</span>
                </div>
                <div className="inline-flex items-center px-2.5 py-0.5 border border-accent-amber/30 bg-accent-amber/10 text-accent-amber text-data font-medium">
                  Developing Capability
                </div>
              </div>

              <div className="col-span-2 space-y-4">
                <div className="flex justify-between items-center py-2 border-b border-border-light">
                  <span className="text-body font-medium text-text-primary">Awareness</span>
                  <span className="text-data text-text-primary">82 / 100</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-border-light">
                  <span className="text-body font-medium text-text-primary">Adoption</span>
                  <span className="text-data text-text-primary">75 / 100</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-border-light">
                  <span className="text-body font-medium text-text-primary">Integration</span>
                  <span className="text-data text-text-primary">68 / 100</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-border-light">
                  <span className="text-body font-medium text-text-primary">ROI</span>
                  <span className="text-data text-text-primary">71 / 100</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-border-light bg-accent-red/5 px-3 -mx-3">
                  <span className="text-body font-medium text-accent-red flex items-center gap-2">
                    <ShieldAlert className="w-4 h-4" />
                    Governance
                  </span>
                  <span className="text-data text-accent-red">42 / 100</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 5. Why Traditional Assessments Miss The Signal */}
      <section className="py-[80px] bg-bg-dark text-text-inverse">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="mb-12">
            <h2 className="text-h2 text-text-inverse mb-4">
              Why Traditional Assessments Miss The Signal
            </h2>
            <p className="text-body text-text-inverse/70 max-w-3xl">
              Conventional approaches measure surface compliance. TarkaX evaluates structural reality.
            </p>
          </div>

          <div className="border border-text-inverse/20 overflow-hidden">
            <div className="grid grid-cols-1 md:grid-cols-2 border-b border-text-inverse/20">
              <div className="p-6 bg-text-inverse/5">
                <h3 className="text-h3 text-text-inverse">Traditional Assessments</h3>
              </div>
              <div className="p-6 bg-text-inverse/10 border-t md:border-t-0 md:border-l border-text-inverse/20">
                <h3 className="text-h3 text-text-inverse flex items-center gap-2">
                  <div className="w-2 h-2 bg-text-inverse"></div>
                  TarkaX Methodology
                </h3>
              </div>
            </div>

            {[
              ['Point-in-time snapshots that age instantly.', 'Continuous diagnostic evaluation of underlying systems.'],
              ['Static, checklist-driven compliance exercises.', 'Pattern-oriented intelligence identifying recurring failure structures.'],
              ['Over-reliance on stated sentiment over actual practice.', 'Focused on operational signals and evidence-based reality.'],
              ['Focused on generating an arbitrary score.', 'Designed exclusively to answer: What decision should we make?']
            ].map(([traditional, tarkax], idx) => (
              <div key={idx} className="grid grid-cols-1 md:grid-cols-2 border-b border-text-inverse/20 last:border-0">
                <div className="p-6 text-body text-text-inverse/70">
                  {traditional}
                </div>
                <div className="p-6 text-body text-text-inverse border-t md:border-t-0 md:border-l border-text-inverse/20 bg-text-inverse/5">
                  {tarkax}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 6. Product Modules */}
      <section className="py-[80px] bg-bg-primary border-b border-border-strong">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <h2 className="text-h2 text-text-primary mb-12">Diagnostic Instruments</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="border border-border-strong p-8 flex flex-col">
              <h3 className="text-h3 text-text-primary mb-4">AI Audit</h3>
              <p className="text-body text-text-secondary mb-8 flex-grow">
                Evaluate organizational readiness for AI deployment across awareness, adoption, integration, governance, and ROI.
              </p>
              <Link to="/ai-audit" className="text-body font-medium text-text-primary hover:underline inline-flex items-center gap-2">
                View Instrument Details <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            <div className="border border-border-strong p-8 flex flex-col">
              <h3 className="text-h3 text-text-primary mb-4">Workflow Diagnostic</h3>
              <p className="text-body text-text-secondary mb-8 flex-grow">
                Identify operational weaknesses, tool bloat, and execution bottlenecks in specific departmental workflows.
              </p>
              <Link to="/workflow-diagnostic" className="text-body font-medium text-text-primary hover:underline inline-flex items-center gap-2">
                View Instrument Details <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* 7. Trust Layer */}
      <section className="py-[60px] bg-bg-secondary border-b border-border-strong">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 text-center">
          <p className="text-label text-text-secondary mb-4">Platform Application Focus</p>
          <div className="text-body text-text-primary max-w-2xl mx-auto">
            Currently developed and validated specifically for management consulting engagements and public sector programmatic oversight.
          </div>
        </div>
      </section>

      {/* 8. FAQ Section */}
      <FAQSection
        title="Frequently Asked Questions"
        faqItems={faqItems}
      />

      {/* 9. Final CTA */}
      <section className="py-[120px] bg-bg-primary text-center">
        <div className="max-w-3xl mx-auto px-6 lg:px-8">
          <h2 className="text-h2 text-text-primary mb-8">
            Establish your operational baseline.
          </h2>
          <Link
            to="/contact"
            className="inline-flex items-center justify-center px-8 py-4 bg-text-primary text-text-inverse text-body font-medium transition-colors hover:bg-text-primary/90 gap-2"
          >
            Request a Demo
          </Link>
        </div>
      </section>
    </div>
  );
}
