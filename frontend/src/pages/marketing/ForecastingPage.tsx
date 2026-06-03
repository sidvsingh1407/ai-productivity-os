import { Link } from 'react-router-dom';
import { ArrowRight, Map } from 'lucide-react';

export default function ForecastingPage() {
  return (
    <div className="bg-bg-primary min-h-[80vh] flex flex-col justify-center animate-fade-up">
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

      {/* Details */}
      <section className="py-[80px] bg-bg-secondary border-t border-border-light mt-auto">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
           <div className="grid grid-cols-1 md:grid-cols-3 gap-space-xl text-center">
              <div>
                 <div className="w-12 h-12 rounded-full bg-bg-primary border border-border-light mx-auto flex items-center justify-center mb-space-sm shadow-subtle">
                   <Map className="w-5 h-5 text-text-secondary" />
                 </div>
                 <h3 className="text-h3 text-text-primary mb-space-xs">Scenario Modeling</h3>
                 <p className="text-body text-text-secondary">Model how organizational changes might impact current risk structures and operational capacity.</p>
              </div>
              <div>
                 <div className="w-12 h-12 rounded-full bg-bg-primary border border-border-light mx-auto flex items-center justify-center mb-space-sm shadow-subtle">
                   <Map className="w-5 h-5 text-text-secondary" />
                 </div>
                 <h3 className="text-h3 text-text-primary mb-space-xs">Trajectory Analysis</h3>
                 <p className="text-body text-text-secondary">Understand the likely trajectory of unmitigated governance or adoption gaps.</p>
              </div>
              <div>
                 <div className="w-12 h-12 rounded-full bg-bg-primary border border-border-light mx-auto flex items-center justify-center mb-space-sm shadow-subtle">
                   <Map className="w-5 h-5 text-text-secondary" />
                 </div>
                 <h3 className="text-h3 text-text-primary mb-space-xs">Planning Considerations</h3>
                 <p className="text-body text-text-secondary">Inform strategic planning with structured insights on operational capacity.</p>
              </div>
           </div>
        </div>
      </section>
    </div>
  );
}