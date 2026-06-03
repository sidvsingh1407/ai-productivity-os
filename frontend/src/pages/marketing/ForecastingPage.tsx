import { Link } from 'react-router-dom';
import { ArrowRight, Map } from 'lucide-react';

export default function ForecastingPage() {
  return (
    <div className="bg-background min-h-[80vh] flex flex-col justify-center">
      {/* Hero */}
      <section className="py-24 bg-background">
        <div className="max-w-4xl mx-auto px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-gray-100 border border-gray-200 text-gray-700 text-xs font-medium rounded-full mb-8 uppercase tracking-wider">
            <span className="w-2 h-2 rounded-full bg-gray-400"></span>
            Upcoming Capability
          </div>
          <h1 className="text-4xl md:text-6xl font-light text-foreground tracking-tight mb-8 leading-[1.1]">
            Understanding what broke is useful. Understanding what could break next is the future.
          </h1>
          <p className="text-xl text-gray-600 font-light leading-relaxed mb-12">
            The Forecasting Framework is an upcoming capability designed for operational scenario modeling, exploring future risk trajectories based on structural realities.
          </p>

          <div className="flex justify-center">
            <Link
              to="/contact?interest=Forecasting+Framework"
              className="inline-flex items-center justify-center px-8 py-4 bg-foreground text-background font-medium rounded-lg hover:bg-foreground/90 transition-all gap-2"
            >
              Request Early Access
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Details */}
      <section className="py-20 bg-gray-50 border-t border-gray-100 mt-auto">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
           <div className="grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
              <div>
                 <div className="w-12 h-12 rounded-full bg-white border border-gray-200 mx-auto flex items-center justify-center mb-6">
                   <Map className="w-5 h-5 text-gray-600" />
                 </div>
                 <h3 className="text-lg font-medium text-foreground mb-3">Scenario Modeling</h3>
                 <p className="text-gray-600 font-light text-sm">Model how organizational changes might impact current risk structures and operational capacity.</p>
              </div>
              <div>
                 <div className="w-12 h-12 rounded-full bg-white border border-gray-200 mx-auto flex items-center justify-center mb-6">
                   <Map className="w-5 h-5 text-gray-600" />
                 </div>
                 <h3 className="text-lg font-medium text-foreground mb-3">Trajectory Analysis</h3>
                 <p className="text-gray-600 font-light text-sm">Understand the likely trajectory of unmitigated governance or adoption gaps.</p>
              </div>
              <div>
                 <div className="w-12 h-12 rounded-full bg-white border border-gray-200 mx-auto flex items-center justify-center mb-6">
                   <Map className="w-5 h-5 text-gray-600" />
                 </div>
                 <h3 className="text-lg font-medium text-foreground mb-3">Planning Considerations</h3>
                 <p className="text-gray-600 font-light text-sm">Inform strategic planning with structured insights on operational capacity.</p>
              </div>
           </div>
        </div>
      </section>
    </div>
  );
}