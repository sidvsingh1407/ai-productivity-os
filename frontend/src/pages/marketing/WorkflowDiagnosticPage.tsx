import { Link } from 'react-router-dom';
import { ArrowRight, AlertTriangle } from 'lucide-react';
import { SeoHead } from '../../components/geo/SeoHead';
import { DefinitionBlock } from '../../components/geo/DefinitionBlock';
import { FAQSection, generateFAQSchema } from '../../components/geo/FAQSection';

export default function WorkflowDiagnosticPage() {
  const faqItems = [
    {
      question: "What is Workflow Intelligence?",
      answer: "Workflow Intelligence is the practice of evaluating operational processes to identify structural weaknesses, hidden friction, and execution gaps. It relies on qualitative inputs and behavioral insights rather than pure system logs to uncover the human realities of how work actually gets done."
    },
    {
      question: "How is Workflow Intelligence different from process mapping?",
      answer: "Process mapping documents the theoretical way a task should be completed. Workflow Intelligence evaluates the actual operational reality, identifying workarounds, shadow IT, and hidden bottlenecks that process maps fail to capture."
    },
    {
      question: "Who should use Workflow Intelligence?",
      answer: "Operations leaders, COOs, and external consultants use Workflow Intelligence to audit complex environments, optimize processes before automation, and identify root causes of operational friction."
    }
  ];

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
        "name": "Workflow Intelligence",
        "item": "https://tarkax.com/workflow-diagnostic"
      }
    ]
  };

  const faqSchema = generateFAQSchema(faqItems);

  return (
    <div className="bg-bg-primary animate-fade-up">
      <SeoHead
        title="Workflow Intelligence | TarkaX"
        description="Evaluate workflow health and identify operational weaknesses systematically with TarkaX Workflow Intelligence."
        canonical="https://tarkax.com/workflow-diagnostic"
        schema={[breadcrumbSchema, faqSchema]}
      />
      {/* Header */}
      <section className="pt-[120px] pb-[80px] bg-bg-secondary border-b border-border-light">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="inline-block px-3 py-1 bg-bg-primary border border-border-light text-text-secondary text-label rounded-full mb-space-md">
            Diagnostic Framework
          </div>
          <h1 className="text-h1 text-text-primary max-w-3xl mb-space-sm">
            Workflow Intelligence
          </h1>

          <div className="mt-8 max-w-3xl w-full">
            <DefinitionBlock
              question="What is a Workflow Intelligence?"
              answer="A Workflow Intelligence is an analytical evaluation of operational processes designed to uncover hidden friction, structural bottlenecks, and behavioral workarounds that impede execution."
            />
          </div>

          <p className="mt-space-md text-h3 font-normal text-text-secondary max-w-2xl">
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
              The Workflow Intelligence provides a structured framework to evaluate processes, identifying friction points and operational gaps before they compound into major failures.
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
          <div className="overflow-x-auto max-w-5xl mx-auto">
            <table className="w-full text-left border-collapse border border-border-light bg-bg-primary rounded-lg shadow-sm">
              <thead>
                <tr className="bg-bg-secondary border-b border-border-light">
                  <th className="py-4 px-6 text-label text-text-secondary font-medium w-1/3">Evaluation Area</th>
                  <th className="py-4 px-6 text-label text-text-secondary font-medium">Diagnostic Objective</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-light text-body text-text-primary">
                <tr>
                  <td className="py-4 px-6 font-medium">Process Consistency</td>
                  <td className="py-4 px-6 text-text-secondary">Assess the variance in how workflows are executed across different teams and identify areas lacking standardization.</td>
                </tr>
                <tr>
                  <td className="py-4 px-6 font-medium">Tool Utilization</td>
                  <td className="py-4 px-6 text-text-secondary">Evaluate if existing systems are being used as intended or if workarounds have become the primary method of execution.</td>
                </tr>
                <tr>
                  <td className="py-4 px-6 font-medium">Information Handoffs</td>
                  <td className="py-4 px-6 text-text-secondary">Identify points where data or responsibility transfers between units, which are common failure points.</td>
                </tr>
                <tr>
                  <td className="py-4 px-6 font-medium">Structural Bottlenecks</td>
                  <td className="py-4 px-6 text-text-secondary">Review the workflow to locate dependencies that consistently delay execution or require manual intervention.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* Example Findings */}
      <section className="py-[80px] bg-bg-primary border-b border-border-light">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <h2 className="text-h2 text-text-primary mb-space-xl text-center">
            Example Findings
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

          <div className="mt-space-xl border-t border-border-light pt-space-lg">
            <h3 className="text-h3 text-text-primary mb-space-sm">Explore Related Products</h3>
            <div className="flex gap-4">
              <Link to="/ai-audit" className="text-accent-blue font-medium hover:underline flex items-center gap-1">
                See Where AI Is Failing <ArrowRight className="w-4 h-4" />
              </Link>
              <Link to="/forecasting" className="text-accent-blue font-medium hover:underline flex items-center gap-1">
                Forecasting Framework <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <FAQSection faqItems={faqItems} />

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