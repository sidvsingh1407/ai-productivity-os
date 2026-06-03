import { Link } from 'react-router-dom';
import { BarChart3, Activity, FastForward, ShieldAlert, ArrowRight } from 'lucide-react';

export default function Home() {
  return (
    <div className="bg-bg-primary">
      {/* 1. Hero Section */}
      <section className="py-[120px] border-b border-border-light bg-bg-primary animate-fade-up">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 flex flex-col items-start">
          <h1 className="text-display text-text-primary max-w-4xl">
            Operational failures rarely arrive without warning.
          </h1>
          <p className="mt-space-md text-h3 font-normal text-text-secondary max-w-3xl">
            TarkaX helps organizations identify AI adoption gaps, workflow weaknesses, governance blind spots, and execution risks before they become larger operational problems.
          </p>
          <div className="mt-space-xl flex flex-col sm:flex-row items-center gap-space-sm">
            <Link
              to="/contact"
              className="px-8 py-4 bg-accent-blue text-text-inverse text-body font-medium rounded-md shadow-sm hover:bg-accent-blue/90 transition-colors flex items-center justify-center gap-2"
            >
              Request a Demo
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* 2. Problem Frame */}
      <section className="py-[80px] bg-bg-secondary border-b border-border-light">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-space-xl">
            <div>
              <h2 className="text-h2 text-text-primary mb-space-md">
                The reality of operational execution
              </h2>
              <p className="text-body text-text-secondary mb-space-sm">
                Most operational failures are visible before they become obvious. The signal often exists long before the problem is acknowledged.
              </p>
            </div>
            <div className="space-y-space-md">
              <div className="border-l-[3px] border-border-strong pl-space-md">
                <p className="text-body text-text-primary font-medium">AI initiatives often underperform before organizations recognize the warning signs.</p>
              </div>
              <div className="border-l-[3px] border-border-strong pl-space-md">
                <p className="text-body text-text-primary font-medium">Workflow breakdowns are usually symptoms of deeper structural issues.</p>
              </div>
              <div className="border-l-[3px] border-border-strong pl-space-md">
                <p className="text-body text-text-primary font-medium">Governance gaps often emerge long before compliance concerns become visible.</p>
              </div>
              <div className="border-l-[3px] border-border-strong pl-space-md">
                <p className="text-body text-text-primary font-medium">Most organizations have the data. Few have the systems to interpret it.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 3. Category Positioning */}
      <section className="py-[80px] bg-bg-primary border-b border-border-light">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 text-center max-w-4xl mx-auto">
          <h2 className="text-label text-text-secondary mb-space-sm">Category Definition</h2>
          <h3 className="text-h1 text-text-primary mb-space-md">
            TarkaX is an Operational Intelligence Platform built on Failure Intelligence principles.
          </h3>
          <p className="text-body text-text-secondary mb-space-lg">
            TarkaX is not a chatbot, a dashboard, or an automation platform. It is a diagnostic system designed to capture the true state of your operational execution.
          </p>
          <div className="flex flex-col md:flex-row items-center justify-center gap-space-md text-h3 text-text-primary font-medium">
            <span className="px-6 py-3 bg-bg-secondary rounded-lg border border-border-light shadow-subtle">Assess</span>
            <ArrowRight className="text-border-strong hidden md:block" />
            <span className="px-6 py-3 bg-bg-secondary rounded-lg border border-border-light shadow-subtle">Diagnose</span>
            <ArrowRight className="text-border-strong hidden md:block" />
            <span className="px-6 py-3 bg-bg-secondary rounded-lg border border-border-light shadow-subtle">Improve</span>
          </div>
        </div>
      </section>

      {/* 4. Product Capabilities */}
      <section className="py-[80px] bg-bg-secondary border-b border-border-light">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <h2 className="text-h2 text-text-primary mb-space-xl text-center">
            Product Capabilities
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-space-lg">
            {/* AI Audit */}
            <div className="bg-bg-primary p-space-md rounded-lg border border-border-light shadow-subtle hover:shadow-card transition-shadow duration-300 flex flex-col">
              <div className="w-12 h-12 rounded-md bg-bg-secondary border border-border-light flex items-center justify-center mb-space-md">
                <BarChart3 className="w-6 h-6 text-text-secondary" />
              </div>
              <h3 className="text-h3 text-text-primary mb-space-sm">AI Audit</h3>
              <div className="mb-space-md flex-grow">
                <p className="text-label text-text-secondary mb-space-xs">Problem solved:</p>
                <p className="text-body text-text-primary mb-space-sm">Understanding organizational AI readiness.</p>
                <p className="text-label text-text-secondary mb-space-xs">Output:</p>
                <p className="text-body text-text-primary">Maturity findings, governance insights, recommendations.</p>
              </div>
              <Link to="/ai-audit" className="text-accent-blue text-body font-medium hover:underline flex items-center gap-space-xs mt-auto">
                Explore Module <ArrowRight className="w-4 h-4" />
              </Link>
            </div>

            {/* Workflow Diagnostic */}
            <div className="bg-bg-primary p-space-md rounded-lg border border-border-light shadow-subtle hover:shadow-card transition-shadow duration-300 flex flex-col">
              <div className="w-12 h-12 rounded-md bg-bg-secondary border border-border-light flex items-center justify-center mb-space-md">
                <Activity className="w-6 h-6 text-text-secondary" />
              </div>
              <h3 className="text-h3 text-text-primary mb-space-sm">Workflow Diagnostic</h3>
              <div className="mb-space-md flex-grow">
                <p className="text-label text-text-secondary mb-space-xs">Problem solved:</p>
                <p className="text-body text-text-primary mb-space-sm">Evaluating workflow health and operational weaknesses.</p>
                <p className="text-label text-text-secondary mb-space-xs">Output:</p>
                <p className="text-body text-text-primary">Diagnostic findings and improvement opportunities.</p>
              </div>
              <Link to="/workflow-diagnostic" className="text-accent-blue text-body font-medium hover:underline flex items-center gap-space-xs mt-auto">
                Explore Module <ArrowRight className="w-4 h-4" />
              </Link>
            </div>

            {/* Forecasting Framework */}
            <div className="bg-bg-primary p-space-md rounded-lg border border-border-light shadow-subtle hover:shadow-card transition-shadow duration-300 flex flex-col relative overflow-hidden">
              <div className="absolute top-6 right-6 bg-bg-secondary text-text-secondary text-label px-2 py-1 rounded">
                Coming Soon
              </div>
              <div className="w-12 h-12 rounded-md bg-bg-secondary border border-border-light flex items-center justify-center mb-space-md opacity-70">
                <FastForward className="w-6 h-6 text-text-secondary" />
              </div>
              <h3 className="text-h3 text-text-primary mb-space-sm opacity-90">Forecasting Framework</h3>
              <div className="mb-space-md flex-grow opacity-90">
                <p className="text-label text-text-secondary mb-space-xs">Problem solved:</p>
                <p className="text-body text-text-primary mb-space-sm">Exploring future operational scenarios.</p>
                <p className="text-label text-text-secondary mb-space-xs">Output:</p>
                <p className="text-body text-text-primary">Potential risk trajectories and planning considerations.</p>
              </div>
              <Link to="/forecasting" className="text-accent-blue text-body font-medium hover:underline flex items-center gap-space-xs mt-auto">
                Explore Capability <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* 5. Who It's For */}
      <section className="py-[80px] bg-bg-primary border-b border-border-light">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-space-xl items-center">
            <div>
              <h2 className="text-h2 text-text-primary mb-space-md">
                Designed for complex operational environments
              </h2>
              <p className="text-body text-text-secondary mb-space-lg">
                TarkaX is built for organizations that require rigorous, evidence-oriented analysis rather than superficial assessments.
              </p>
            </div>
            <div className="space-y-space-sm">
              <div className="p-space-md bg-bg-secondary rounded-lg border border-border-light shadow-subtle">
                <h4 className="text-body font-medium text-text-primary mb-space-xs">Consulting Firms</h4>
                <p className="text-body text-text-secondary">Operationalize diagnostics and standardize failure intelligence across your client portfolio.</p>
              </div>
              <div className="p-space-md bg-bg-secondary rounded-lg border border-border-light shadow-subtle">
                <h4 className="text-body font-medium text-text-primary mb-space-xs">Government & Public Sector Organizations</h4>
                <p className="text-body text-text-secondary">Evaluate programmatic risk, governance blind spots, and alignment with policy objectives securely.</p>
              </div>
              <div className="p-space-md bg-bg-secondary rounded-lg border border-border-light shadow-subtle">
                <h4 className="text-body font-medium text-text-primary mb-space-xs">Enterprise Operations Teams</h4>
                <p className="text-body text-text-secondary">Establish a quantitative baseline for operational realities to prioritize interventions.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 6. Why Traditional Assessments Miss The Signal (MANDATORY) */}
      <section className="py-[80px] bg-bg-dark text-text-inverse">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="text-center mb-space-xl">
            <h2 className="text-h2 text-text-inverse mb-space-md">
              Why Traditional Assessments Miss The Signal
            </h2>
            <p className="text-body text-text-inverse/70 max-w-3xl mx-auto">
              Conventional approaches measure surface compliance. TarkaX evaluates structural reality.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-space-lg">
            <div className="bg-text-inverse/5 p-space-lg rounded-lg border border-text-inverse/10">
              <h3 className="text-h3 text-text-inverse mb-space-md flex items-center gap-3">
                <ShieldAlert className="w-5 h-5 text-text-inverse/50" />
                Traditional Assessments
              </h3>
              <ul className="space-y-space-sm text-body text-text-inverse/70">
                <li className="flex items-start gap-3"><span className="text-text-inverse/30 mt-1">―</span> Point-in-time snapshots that age instantly.</li>
                <li className="flex items-start gap-3"><span className="text-text-inverse/30 mt-1">―</span> Static, checklist-driven compliance exercises.</li>
                <li className="flex items-start gap-3"><span className="text-text-inverse/30 mt-1">―</span> Over-reliance on stated sentiment over actual practice.</li>
                <li className="flex items-start gap-3"><span className="text-text-inverse/30 mt-1">―</span> Focused on generating a score rather than a decision.</li>
              </ul>
            </div>
            <div className="bg-bg-primary text-text-primary p-space-lg rounded-lg shadow-card border border-border-light">
              <h3 className="text-h3 text-text-primary mb-space-md flex items-center gap-3">
                <div className="w-4 h-4 bg-text-primary rounded-sm"></div>
                TarkaX Methodology
              </h3>
              <ul className="space-y-space-sm text-body text-text-secondary">
                <li className="flex items-start gap-3"><span className="text-border-strong mt-1">―</span> Diagnostic, evaluating the health of the underlying system.</li>
                <li className="flex items-start gap-3"><span className="text-border-strong mt-1">―</span> Pattern-oriented, identifying recurring failure structures.</li>
                <li className="flex items-start gap-3"><span className="text-border-strong mt-1">―</span> Focused on operational signals and evidence-based reality.</li>
                <li className="flex items-start gap-3"><span className="text-border-strong mt-1">―</span> Designed exclusively to answer: What decision should we make?</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* 7. Trust Layer */}
      <section className="py-[80px] bg-bg-secondary border-b border-border-light">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 text-center">
          <p className="text-label text-text-secondary mb-space-md">Platform Status</p>
          <div className="inline-flex items-center gap-3 px-6 py-3 bg-bg-primary border border-border-light rounded-full text-body text-text-primary shadow-subtle">
            <span className="w-2 h-2 rounded-full bg-border-strong"></span>
            Currently being developed and validated with a focus on consulting and public sector use cases.
          </div>
        </div>
      </section>

      {/* 8. Final CTA */}
      <section className="py-[120px] bg-bg-primary text-center">
        <div className="max-w-3xl mx-auto px-6 lg:px-8">
          <h2 className="text-h1 text-text-primary mb-space-lg">
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