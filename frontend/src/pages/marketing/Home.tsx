import { Link } from 'react-router-dom';
import { BarChart3, Activity, FastForward, ShieldAlert, ArrowRight } from 'lucide-react';

export default function Home() {
  return (
    <div className="bg-background">
      {/* 1. Hero Section */}
      <section className="pt-24 pb-32 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 flex flex-col items-start">
          <h1 className="text-5xl md:text-6xl font-light text-foreground tracking-tight leading-[1.1] max-w-4xl">
            Operational failures rarely arrive without warning.
          </h1>
          <p className="mt-8 text-xl text-gray-600 font-light max-w-3xl leading-relaxed">
            TarkaX helps organizations identify AI adoption gaps, workflow weaknesses, governance blind spots, and execution risks before they become larger operational problems.
          </p>
          <div className="mt-12 flex flex-col sm:flex-row items-center gap-4">
            <Link
              to="/contact"
              className="px-8 py-4 bg-foreground text-background font-medium rounded-lg hover:bg-foreground/90 transition-all flex items-center justify-center gap-2"
            >
              Request a Demo
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* 2. Problem Frame */}
      <section className="py-24 bg-gray-50/50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-16">
            <div>
              <h2 className="text-3xl font-light text-foreground tracking-tight mb-8">
                The reality of operational execution
              </h2>
              <p className="text-lg text-gray-600 font-light leading-relaxed mb-6">
                Most operational failures are visible before they become obvious. The signal often exists long before the problem is acknowledged.
              </p>
            </div>
            <div className="space-y-8">
              <div className="border-l-2 border-gray-200 pl-6">
                <p className="text-lg text-foreground font-medium mb-2">AI initiatives often underperform before organizations recognize the warning signs.</p>
              </div>
              <div className="border-l-2 border-gray-200 pl-6">
                <p className="text-lg text-foreground font-medium mb-2">Workflow breakdowns are usually symptoms of deeper structural issues.</p>
              </div>
              <div className="border-l-2 border-gray-200 pl-6">
                <p className="text-lg text-foreground font-medium mb-2">Governance gaps often emerge long before compliance concerns become visible.</p>
              </div>
              <div className="border-l-2 border-gray-200 pl-6">
                <p className="text-lg text-foreground font-medium mb-2">Most organizations have the data. Few have the systems to interpret it.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 3. Category Positioning */}
      <section className="py-24 bg-background border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 text-center max-w-4xl mx-auto">
          <h2 className="text-xl font-medium text-gray-500 tracking-tight mb-4 uppercase text-sm">Category Definition</h2>
          <h3 className="text-4xl font-light text-foreground tracking-tight mb-8">
            TarkaX is an Operational Intelligence Platform built on Failure Intelligence principles.
          </h3>
          <p className="text-lg text-gray-600 font-light leading-relaxed mb-12">
            TarkaX is not a chatbot, a dashboard, or an automation platform. It is a diagnostic system designed to capture the true state of your operational execution.
          </p>
          <div className="flex flex-col md:flex-row items-center justify-center gap-4 md:gap-8 font-medium text-foreground text-lg">
            <span className="px-6 py-3 bg-gray-50 rounded-lg border border-gray-100">Assess</span>
            <ArrowRight className="text-gray-300 hidden md:block" />
            <span className="px-6 py-3 bg-gray-50 rounded-lg border border-gray-100">Diagnose</span>
            <ArrowRight className="text-gray-300 hidden md:block" />
            <span className="px-6 py-3 bg-gray-50 rounded-lg border border-gray-100">Improve</span>
          </div>
        </div>
      </section>

      {/* 4. Product Capabilities */}
      <section className="py-24 bg-gray-50/50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <h2 className="text-3xl font-light text-foreground tracking-tight mb-16 text-center">
            Product Capabilities
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* AI Audit */}
            <div className="bg-white p-8 rounded-xl border border-gray-200 shadow-sm flex flex-col">
              <div className="w-12 h-12 rounded-lg bg-gray-50 border border-gray-100 flex items-center justify-center mb-6">
                <BarChart3 className="w-6 h-6 text-foreground" />
              </div>
              <h3 className="text-2xl font-medium text-foreground mb-4">AI Audit</h3>
              <div className="mb-6 flex-grow">
                <p className="text-sm font-medium text-gray-500 mb-1">Problem solved:</p>
                <p className="text-gray-800 font-light mb-4">Understanding organizational AI readiness.</p>
                <p className="text-sm font-medium text-gray-500 mb-1">Output:</p>
                <p className="text-gray-800 font-light">Maturity findings, governance insights, recommendations.</p>
              </div>
              <Link to="/ai-audit" className="text-foreground font-medium hover:underline flex items-center gap-2 mt-auto">
                Explore Module <ArrowRight className="w-4 h-4" />
              </Link>
            </div>

            {/* Workflow Diagnostic */}
            <div className="bg-white p-8 rounded-xl border border-gray-200 shadow-sm flex flex-col">
              <div className="w-12 h-12 rounded-lg bg-gray-50 border border-gray-100 flex items-center justify-center mb-6">
                <Activity className="w-6 h-6 text-foreground" />
              </div>
              <h3 className="text-2xl font-medium text-foreground mb-4">Workflow Diagnostic</h3>
              <div className="mb-6 flex-grow">
                <p className="text-sm font-medium text-gray-500 mb-1">Problem solved:</p>
                <p className="text-gray-800 font-light mb-4">Evaluating workflow health and operational weaknesses.</p>
                <p className="text-sm font-medium text-gray-500 mb-1">Output:</p>
                <p className="text-gray-800 font-light">Diagnostic findings and improvement opportunities.</p>
              </div>
              <Link to="/workflow-diagnostic" className="text-foreground font-medium hover:underline flex items-center gap-2 mt-auto">
                Explore Module <ArrowRight className="w-4 h-4" />
              </Link>
            </div>

            {/* Forecasting Framework */}
            <div className="bg-white p-8 rounded-xl border border-gray-200 shadow-sm flex flex-col relative overflow-hidden">
              <div className="absolute top-6 right-6 bg-gray-100 text-gray-600 text-xs font-medium px-2 py-1 rounded">
                Coming Soon
              </div>
              <div className="w-12 h-12 rounded-lg bg-gray-50 border border-gray-100 flex items-center justify-center mb-6 opacity-70">
                <FastForward className="w-6 h-6 text-foreground" />
              </div>
              <h3 className="text-2xl font-medium text-foreground mb-4 opacity-90">Forecasting Framework</h3>
              <div className="mb-6 flex-grow opacity-90">
                <p className="text-sm font-medium text-gray-500 mb-1">Problem solved:</p>
                <p className="text-gray-800 font-light mb-4">Exploring future operational scenarios.</p>
                <p className="text-sm font-medium text-gray-500 mb-1">Output:</p>
                <p className="text-gray-800 font-light">Potential risk trajectories and planning considerations.</p>
              </div>
              <Link to="/forecasting" className="text-foreground font-medium hover:underline flex items-center gap-2 mt-auto">
                Explore Capability <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* 5. Who It's For */}
      <section className="py-24 bg-background border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-3xl font-light text-foreground tracking-tight mb-6">
                Designed for complex operational environments
              </h2>
              <p className="text-lg text-gray-600 font-light leading-relaxed mb-8">
                TarkaX is built for organizations that require rigorous, evidence-oriented analysis rather than superficial assessments.
              </p>
            </div>
            <div className="space-y-4">
              <div className="p-6 bg-gray-50 rounded-xl border border-gray-100">
                <h4 className="text-lg font-medium text-foreground mb-2">Consulting Firms</h4>
                <p className="text-gray-600 font-light">Operationalize diagnostics and standardize failure intelligence across your client portfolio.</p>
              </div>
              <div className="p-6 bg-gray-50 rounded-xl border border-gray-100">
                <h4 className="text-lg font-medium text-foreground mb-2">Government & Public Sector Organizations</h4>
                <p className="text-gray-600 font-light">Evaluate programmatic risk, governance blind spots, and alignment with policy objectives securely.</p>
              </div>
              <div className="p-6 bg-gray-50 rounded-xl border border-gray-100">
                <h4 className="text-lg font-medium text-foreground mb-2">Enterprise Operations Teams</h4>
                <p className="text-gray-600 font-light">Establish a quantitative baseline for operational realities to prioritize interventions.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 6. Why Traditional Assessments Miss The Signal (MANDATORY) */}
      <section className="py-24 bg-foreground text-background">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-light tracking-tight mb-6">
              Why Traditional Assessments Miss The Signal
            </h2>
            <p className="text-lg text-gray-400 font-light leading-relaxed max-w-3xl mx-auto">
              Conventional approaches measure surface compliance. TarkaX evaluates structural reality.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
            <div className="bg-background/10 p-8 rounded-xl border border-background/20">
              <h3 className="text-xl font-medium mb-6 flex items-center gap-3">
                <ShieldAlert className="w-5 h-5 text-gray-400" />
                Traditional Assessments
              </h3>
              <ul className="space-y-4 text-gray-300 font-light">
                <li className="flex items-start gap-3"><span className="text-gray-500 mt-1">―</span> Point-in-time snapshots that age instantly.</li>
                <li className="flex items-start gap-3"><span className="text-gray-500 mt-1">―</span> Static, checklist-driven compliance exercises.</li>
                <li className="flex items-start gap-3"><span className="text-gray-500 mt-1">―</span> Over-reliance on stated sentiment over actual practice.</li>
                <li className="flex items-start gap-3"><span className="text-gray-500 mt-1">―</span> Focused on generating a score rather than a decision.</li>
              </ul>
            </div>
            <div className="bg-background text-foreground p-8 rounded-xl shadow-lg border border-gray-200">
              <h3 className="text-xl font-medium mb-6 flex items-center gap-3">
                <div className="w-4 h-4 bg-foreground rounded-sm"></div>
                TarkaX Methodology
              </h3>
              <ul className="space-y-4 text-gray-600 font-light">
                <li className="flex items-start gap-3"><span className="text-gray-300 mt-1">―</span> Diagnostic, evaluating the health of the underlying system.</li>
                <li className="flex items-start gap-3"><span className="text-gray-300 mt-1">―</span> Pattern-oriented, identifying recurring failure structures.</li>
                <li className="flex items-start gap-3"><span className="text-gray-300 mt-1">―</span> Focused on operational signals and evidence-based reality.</li>
                <li className="flex items-start gap-3"><span className="text-gray-300 mt-1">―</span> Designed exclusively to answer: What decision should we make?</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* 7. Trust Layer */}
      <section className="py-20 bg-gray-50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 text-center">
          <p className="text-gray-500 font-medium text-sm tracking-widest uppercase mb-8">Platform Status</p>
          <div className="inline-flex items-center gap-3 px-6 py-3 bg-white border border-gray-200 rounded-full text-gray-700 font-medium shadow-sm">
            <span className="w-2 h-2 rounded-full bg-gray-400"></span>
            Currently being developed and validated with a focus on consulting and public sector use cases.
          </div>
        </div>
      </section>

      {/* 8. Final CTA */}
      <section className="py-32 bg-background text-center">
        <div className="max-w-3xl mx-auto px-6 lg:px-8">
          <h2 className="text-4xl font-light text-foreground tracking-tight mb-8">
            Evaluate your operational reality.
          </h2>
          <Link
            to="/contact"
            className="inline-flex items-center justify-center px-8 py-4 bg-foreground text-background font-medium rounded-lg hover:bg-foreground/90 transition-all gap-2"
          >
            Request a Demo
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>
    </div>
  );
}