import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="bg-background">
      {/* Header */}
      <section className="pt-24 pb-16 border-b border-gray-100">
        <div className="max-w-4xl mx-auto px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-light text-foreground tracking-tight mb-6">
            About TarkaX
          </h1>
          <p className="text-xl text-gray-600 font-light leading-relaxed">
            Building the intelligence layer for organizational execution.
          </p>
        </div>
      </section>

      {/* Content */}
      <section className="py-20 bg-background">
        <div className="max-w-3xl mx-auto px-6 lg:px-8 space-y-16">

          {/* Why TarkaX Exists */}
          <div>
            <h2 className="text-2xl font-light text-foreground tracking-tight mb-6">Why TarkaX Exists</h2>
            <div className="prose prose-gray max-w-none text-gray-600 font-light leading-relaxed space-y-4">
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
            <h2 className="text-2xl font-light text-foreground tracking-tight mb-6">The Category Perspective</h2>
            <div className="prose prose-gray max-w-none text-gray-600 font-light leading-relaxed space-y-4">
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
            <h2 className="text-2xl font-light text-foreground tracking-tight mb-6">The Builder</h2>
            <div className="prose prose-gray max-w-none text-gray-600 font-light leading-relaxed space-y-4">
              <p>
                Work across business analysis, operational research, and AI adoption initiatives revealed a recurring pattern: organizations often struggled to identify early signals of operational weakness.
              </p>
              <p>
                Despite having the data, the intelligence required to interpret that data into diagnostic insights was missing. TarkaX was developed to bridge this gap, translating operational noise into clear, actionable intelligence.
              </p>
            </div>
          </div>

          {/* What Comes Next */}
          <div className="p-8 bg-gray-50 border border-gray-200 rounded-xl">
            <h2 className="text-xl font-medium text-foreground tracking-tight mb-4">What Comes Next</h2>
            <p className="text-gray-600 font-light leading-relaxed">
              Our vision is to move from point-in-time assessments toward continuous operational intelligence. We are building the foundational diagnostics today to support the automated, real-time organizational observability systems of tomorrow.
            </p>
          </div>

        </div>
      </section>

      {/* CTA */}
      <section className="py-24 bg-foreground text-background text-center">
        <div className="max-w-3xl mx-auto px-6 lg:px-8">
          <h2 className="text-3xl font-light tracking-tight mb-8">
            Evaluate your operational reality.
          </h2>
          <Link
            to="/contact"
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