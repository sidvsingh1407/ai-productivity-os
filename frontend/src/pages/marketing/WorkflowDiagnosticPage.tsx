import { Link } from 'react-router-dom';
import { ArrowRight, AlertTriangle } from 'lucide-react';

export default function WorkflowDiagnosticPage() {
  return (
    <div className="bg-bg-primary animate-fade-up">
      {/* Header */}
      <section className="pt-[120px] pb-[80px] bg-bg-secondary border-b border-border-light">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="inline-block px-3 py-1 bg-bg-primary border border-border-light text-text-secondary text-label rounded-full mb-space-md">
            Diagnostic Framework
          </div>
          <h1 className="text-h1 text-text-primary max-w-3xl mb-space-sm">
            Workflow Diagnostic
          </h1>
          <p className="text-h3 font-normal text-text-secondary max-w-2xl">
            Evaluate workflow health and identify operational weaknesses systematically.
          </p>
        </div>
      </section>

      {/* Problem */}
      <section className="py-[80px] bg-bg-primary border-b border-border-light">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 grid grid-cols-1 md:grid-cols-3 gap-space-xl">
          <div className="col-span-1">
            <h2 className="text-h2 text-text-primary">The Problem</h2>
          </div>
          <div className="col-span-2">
            <p className="text-body text-text-secondary mb-space-sm">
              Organizations struggle to identify where processes actually break down. Inefficiencies are often treated as isolated incidents rather than symptoms of systemic structural weaknesses.
            </p>
            <p className="text-body text-text-secondary">
              The Workflow Diagnostic provides a structured framework to evaluate processes, identifying friction points and operational gaps before they compound into major failures.
            </p>
          </div>
        </div>
      </section>

      {/* Evaluation Areas */}
      <section className="py-[80px] bg-bg-secondary border-b border-border-light">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <h2 className="text-h2 text-text-primary mb-space-xl text-center">
            Evaluation Areas
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-space-lg max-w-4xl mx-auto">
             <div className="bg-bg-primary p-space-md rounded-lg border border-border-light shadow-subtle">
                <h3 className="text-h3 text-text-primary mb-space-xs">Process Consistency</h3>
                <p className="text-body text-text-secondary">Assess the variance in how workflows are executed across different teams and identify areas lacking standardization.</p>
             </div>
             <div className="bg-bg-primary p-space-md rounded-lg border border-border-light shadow-subtle">
                <h3 className="text-h3 text-text-primary mb-space-xs">Tool Utilization</h3>
                <p className="text-body text-text-secondary">Evaluate if existing systems are being used as intended or if workarounds have become the primary method of execution.</p>
             </div>
             <div className="bg-bg-primary p-space-md rounded-lg border border-border-light shadow-subtle">
                <h3 className="text-h3 text-text-primary mb-space-xs">Information Handoffs</h3>
                <p className="text-body text-text-secondary">Identify points where data or responsibility transfers between units, which are common failure points.</p>
             </div>
             <div className="bg-bg-primary p-space-md rounded-lg border border-border-light shadow-subtle">
                <h3 className="text-h3 text-text-primary mb-space-xs">Structural Bottlenecks</h3>
                <p className="text-body text-text-secondary">Review the workflow to locate dependencies that consistently delay execution or require manual intervention.</p>
             </div>
          </div>
        </div>
      </section>

      {/* Sample Findings */}
      <section className="py-[80px] bg-bg-primary border-b border-border-light">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <h2 className="text-h2 text-text-primary mb-space-xl text-center">
            Sample Findings
          </h2>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-space-lg">
             <div className="p-space-md border border-border-light bg-bg-secondary rounded-lg shadow-subtle">
               <div className="w-10 h-10 bg-bg-primary rounded-md flex items-center justify-center mb-space-sm border border-border-light">
                 <AlertTriangle className="w-5 h-5 text-text-secondary" />
               </div>
               <h4 className="text-h3 text-text-primary mb-space-xs">Shadow Processes</h4>
               <p className="text-body text-text-secondary">Diagnostic reveals that 40% of critical data entry bypasses the primary CRM in favor of localized spreadsheets.</p>
             </div>
             <div className="p-space-md border border-border-light bg-bg-secondary rounded-lg shadow-subtle">
               <div className="w-10 h-10 bg-bg-primary rounded-md flex items-center justify-center mb-space-sm border border-border-light">
                 <AlertTriangle className="w-5 h-5 text-text-secondary" />
               </div>
               <h4 className="text-h3 text-text-primary mb-space-xs">Approval Friction</h4>
               <p className="text-body text-text-secondary">Identifies that secondary approval tiers add an average of 48 hours to execution time without materially reducing risk.</p>
             </div>
             <div className="p-space-md border border-border-light bg-bg-secondary rounded-lg shadow-subtle">
               <div className="w-10 h-10 bg-bg-primary rounded-md flex items-center justify-center mb-space-sm border border-border-light">
                 <AlertTriangle className="w-5 h-5 text-text-secondary" />
               </div>
               <h4 className="text-h3 text-text-primary mb-space-xs">Siloed Knowledge</h4>
               <p className="text-body text-text-secondary">Highlights that workflow completion is entirely dependent on the undocumented institutional knowledge of a single role.</p>
             </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-[120px] bg-bg-dark text-text-inverse text-center">
        <div className="max-w-3xl mx-auto px-6 lg:px-8">
          <h2 className="text-h2 tracking-tight mb-space-lg">
            Evaluate your operational workflows.
          </h2>
          <Link
            to="/contact?interest=Workflow+Diagnostic"
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