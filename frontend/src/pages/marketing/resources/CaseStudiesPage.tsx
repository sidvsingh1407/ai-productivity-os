import { Link } from 'react-router-dom';
import { SeoHead } from '../../../components/geo/SeoHead';
import { BarChart3 } from 'lucide-react';

export default function CaseStudiesPage() {
  return (
    <div className="bg-bg-primary min-h-[70vh] flex flex-col items-center justify-center p-6 text-center">
      <SeoHead title="Case Studies | TarkaX" description="Coming soon: TarkaX case studies." />
      <div className="w-16 h-16 bg-bg-secondary rounded-full flex items-center justify-center mx-auto mb-6">
        <BarChart3 className="w-8 h-8 text-accent-blue" />
      </div>
      <h1 className="text-h2 font-bold text-text-primary mb-4">Case Studies</h1>
      <p className="text-body text-text-secondary max-w-lg mx-auto mb-8">
        Explore how forward-thinking organizations use TarkaX to discover hidden bottlenecks and optimize AI ROI.
      </p>
      <div className="inline-flex items-center px-3 py-1 bg-accent-blue/10 text-accent-blue font-mono text-sm uppercase tracking-wider rounded">
        Coming Soon
      </div>
      <div className="mt-12">
        <Link to="/example-findings" className="text-accent-blue font-medium hover:underline">View Example Findings instead</Link>
      </div>
    </div>
  );
}
