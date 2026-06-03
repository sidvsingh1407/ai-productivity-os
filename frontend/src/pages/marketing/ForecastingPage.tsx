import { Link } from 'react-router-dom';
import { ArrowRight, Map } from 'lucide-react';
import { SeoHead } from '../../components/geo/SeoHead';
import { DefinitionBlock } from '../../components/geo/DefinitionBlock';

export default function ForecastingPage() {
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
        "name": "Forecasting Framework",
        "item": "https://tarkax.com/forecasting"
      }
    ]
  };

  return (
    <div className="bg-bg-primary min-h-[80vh] flex flex-col justify-center animate-fade-up">
      <SeoHead
        title="Forecasting Framework | TarkaX"
        description="The TarkaX Forecasting Framework is an upcoming capability designed for operational scenario modeling and future risk trajectory analysis."
        canonical="https://tarkax.com/forecasting"
        schema={[breadcrumbSchema]}
      />
      {/* Hero */}
      <section className="py-[120px] bg-bg-primary">
        <div className="max-w-4xl mx-auto px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-bg-secondary border border-border-light text-text-secondary text-label rounded-full mb-space-md">
            <span className="w-2 h-2 rounded-full bg-border-strong"></span>
            Upcoming Capability
          </div>
          <h1 className="text-display text-text-primary mb-space-md">
            Understanding what broke is useful. Understanding what could break next is the future.
          </h1>

          <div className="mt-8 mb-8 w-full text-left">
            <DefinitionBlock
              question="What is the Forecasting Framework?"
              answer="The Forecasting Framework is an upcoming predictive capability within TarkaX. It uses baseline assessment data from the AI Audit and Workflow Diagnostic to model potential risk trajectories and organizational capacity."
            />
          </div>

          <p className="text-h3 font-normal text-text-secondary mb-space-lg">
            The Forecasting Framework is an upcoming capability designed for operational scenario modeling, exploring future risk trajectories based on structural realities.
          </p>

          <div className="flex justify-center">
            <Link
              to="/contact?interest=Forecasting+Framework"
              className="inline-flex items-center justify-center px-8 py-4 bg-accent-blue text-text-inverse text-body font-medium rounded-md shadow-sm hover:bg-accent-blue/90 transition-colors gap-2"
            >
              Request Early Access
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Details (Table Format) */}
      <section className="py-[80px] bg-bg-secondary border-t border-border-light mt-auto">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
           <h2 className="text-h2 text-text-primary mb-space-xl text-center">Capability Roadmap</h2>
           <div className="overflow-x-auto max-w-4xl mx-auto">
            <table className="w-full text-left border-collapse border border-border-light bg-bg-primary rounded-lg shadow-sm">
              <thead>
                <tr className="bg-bg-secondary border-b border-border-light">
                  <th className="py-4 px-6 text-label text-text-secondary font-medium w-1/3">Capability</th>
                  <th className="py-4 px-6 text-label text-text-secondary font-medium">Description</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-light text-body text-text-primary">
                <tr>
                  <td className="py-4 px-6 font-medium">Scenario Modeling</td>
                  <td className="py-4 px-6 text-text-secondary">Model how organizational changes might impact current risk structures and operational capacity.</td>
                </tr>
                <tr>
                  <td className="py-4 px-6 font-medium">Trajectory Analysis</td>
                  <td className="py-4 px-6 text-text-secondary">Understand the likely trajectory of unmitigated governance or adoption gaps over time.</td>
                </tr>
                <tr>
                  <td className="py-4 px-6 font-medium">Planning Considerations</td>
                  <td className="py-4 px-6 text-text-secondary">Inform strategic planning with structured insights on future operational capacity and requirements.</td>
                </tr>
              </tbody>
            </table>
           </div>

           <div className="mt-space-xl pt-space-lg text-center">
             <Link to="/ai-audit" className="text-accent-blue font-medium hover:underline inline-flex items-center gap-1">
                Explore Current AI Audit Capabilities <ArrowRight className="w-4 h-4" />
             </Link>
           </div>
        </div>
      </section>
    </div>
  );
}