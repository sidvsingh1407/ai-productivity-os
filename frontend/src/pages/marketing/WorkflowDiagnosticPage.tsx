import { Link } from 'react-router-dom';
import { ArrowRight, AlertTriangle } from 'lucide-react';

export default function WorkflowDiagnosticPage() {
  return (
    <div className="bg-background">
      {/* Header */}
      <section className="pt-24 pb-16 bg-gray-50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="inline-block px-3 py-1 bg-white border border-gray-200 text-gray-600 text-xs font-medium rounded-full mb-6 uppercase tracking-wider">
            Diagnostic Framework
          </div>
          <h1 className="text-4xl md:text-5xl font-light text-foreground tracking-tight max-w-3xl mb-6">
            Workflow Diagnostic
          </h1>
          <p className="text-xl text-gray-600 font-light max-w-2xl leading-relaxed">
            Evaluate workflow health and identify operational weaknesses systematically.
          </p>
        </div>
      </section>

      {/* Problem */}
      <section className="py-20 bg-background border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 grid grid-cols-1 md:grid-cols-3 gap-12">
          <div className="col-span-1">
            <h2 className="text-2xl font-light text-foreground tracking-tight">The Problem</h2>
          </div>
          <div className="col-span-2">
            <p className="text-lg text-gray-600 font-light leading-relaxed mb-6">
              Organizations struggle to identify where processes actually break down. Inefficiencies are often treated as isolated incidents rather than symptoms of systemic structural weaknesses.
            </p>
            <p className="text-lg text-gray-600 font-light leading-relaxed">
              The Workflow Diagnostic provides a structured framework to evaluate processes, identifying friction points and operational gaps before they compound into major failures.
            </p>
          </div>
        </div>
      </section>

      {/* Evaluation Areas */}
      <section className="py-20 bg-gray-50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <h2 className="text-3xl font-light text-foreground tracking-tight mb-12 text-center">
            Evaluation Areas
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
             <div className="bg-white p-8 rounded-xl border border-gray-200 shadow-sm">
                <h3 className="text-xl font-medium text-foreground mb-4">Process Consistency</h3>
                <p className="text-gray-600 font-light">Assess the variance in how workflows are executed across different teams and identify areas lacking standardization.</p>
             </div>
             <div className="bg-white p-8 rounded-xl border border-gray-200 shadow-sm">
                <h3 className="text-xl font-medium text-foreground mb-4">Tool Utilization</h3>
                <p className="text-gray-600 font-light">Evaluate if existing systems are being used as intended or if workarounds have become the primary method of execution.</p>
             </div>
             <div className="bg-white p-8 rounded-xl border border-gray-200 shadow-sm">
                <h3 className="text-xl font-medium text-foreground mb-4">Information Handoffs</h3>
                <p className="text-gray-600 font-light">Identify points where data or responsibility transfers between units, which are common failure points.</p>
             </div>
             <div className="bg-white p-8 rounded-xl border border-gray-200 shadow-sm">
                <h3 className="text-xl font-medium text-foreground mb-4">Structural Bottlenecks</h3>
                <p className="text-gray-600 font-light">Review the workflow to locate dependencies that consistently delay execution or require manual intervention.</p>
             </div>
          </div>
        </div>
      </section>

      {/* Sample Findings */}
      <section className="py-20 bg-background border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <h2 className="text-3xl font-light text-foreground tracking-tight mb-12 text-center">
            Sample Findings
          </h2>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
             <div className="p-6 border border-gray-200 rounded-xl">
               <div className="w-10 h-10 bg-gray-50 rounded-lg flex items-center justify-center mb-4">
                 <AlertTriangle className="w-5 h-5 text-foreground" />
               </div>
               <h4 className="text-lg font-medium text-foreground mb-2">Shadow Processes</h4>
               <p className="text-sm text-gray-600 font-light">Diagnostic reveals that 40% of critical data entry bypasses the primary CRM in favor of localized spreadsheets.</p>
             </div>
             <div className="p-6 border border-gray-200 rounded-xl">
               <div className="w-10 h-10 bg-gray-50 rounded-lg flex items-center justify-center mb-4">
                 <AlertTriangle className="w-5 h-5 text-foreground" />
               </div>
               <h4 className="text-lg font-medium text-foreground mb-2">Approval Friction</h4>
               <p className="text-sm text-gray-600 font-light">Identifies that secondary approval tiers add an average of 48 hours to execution time without materially reducing risk.</p>
             </div>
             <div className="p-6 border border-gray-200 rounded-xl">
               <div className="w-10 h-10 bg-gray-50 rounded-lg flex items-center justify-center mb-4">
                 <AlertTriangle className="w-5 h-5 text-foreground" />
               </div>
               <h4 className="text-lg font-medium text-foreground mb-2">Siloed Knowledge</h4>
               <p className="text-sm text-gray-600 font-light">Highlights that workflow completion is entirely dependent on the undocumented institutional knowledge of a single role.</p>
             </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 bg-foreground text-background text-center">
        <div className="max-w-3xl mx-auto px-6 lg:px-8">
          <h2 className="text-3xl font-light tracking-tight mb-8">
            Evaluate your operational workflows.
          </h2>
          <Link
            to="/contact?interest=Workflow+Diagnostic"
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