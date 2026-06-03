import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="bg-bg-primary">
      {/* Header */}
      <section className="py-[120px] border-b border-border-light bg-bg-secondary animate-fade-up">
        <div className="max-w-4xl mx-auto px-6 lg:px-8 text-center">
          <h1 className="text-h1 text-text-primary mb-space-sm">
            About TarkaX
          </h1>
          <p className="text-h3 font-normal text-text-secondary">
            Building the intelligence layer for organizational execution.
          </p>
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
            <h2 className="text-h2 text-text-primary mb-space-md">The Category Perspective</h2>
            <div className="text-body text-text-secondary space-y-space-sm">
              <p>
                We believe in Operational Intelligence over superficial dashboards. The market is saturated with tools that count activities. TarkaX is built to evaluate execution.
              </p>
              <p>
                We operate on the methodology of Failure Intelligence—the discipline of studying how and why operations break down, and engineering systems to detect those patterns before they manifest as business failure.
              </p>
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
          <div className="p-space-lg bg-bg-secondary border border-border-light rounded-lg shadow-subtle">
            <h2 className="text-h3 text-text-primary mb-space-sm">What Comes Next</h2>
            <p className="text-body text-text-secondary">
              Our vision is to move from point-in-time assessments toward continuous operational intelligence. We are building the foundational diagnostics today to support the automated, real-time organizational observability systems of tomorrow.
            </p>
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