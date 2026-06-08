import { Link } from 'react-router-dom';
import { SeoHead } from '../../../components/geo/SeoHead';
import { BookOpen } from 'lucide-react';

export default function GuidesPage() {
  return (
    <div className="bg-bg-primary min-h-[70vh] flex flex-col items-center justify-center p-6 text-center">
      <SeoHead title="Guides | TarkaX" description="Coming soon: Detailed guides on operational intelligence." />
      <div className="w-16 h-16 bg-bg-secondary rounded-full flex items-center justify-center mx-auto mb-6">
        <BookOpen className="w-8 h-8 text-accent-blue" />
      </div>
      <h1 className="text-h2 font-bold text-text-primary mb-4">Operational Guides</h1>
      <p className="text-body text-text-secondary max-w-lg mx-auto mb-8">
        We are currently developing comprehensive guides on how to implement Failure Intelligence frameworks within your organization.
      </p>
      <div className="inline-flex items-center px-3 py-1 bg-accent-blue/10 text-accent-blue font-mono text-sm uppercase tracking-wider rounded">
        Coming Soon
      </div>
      <div className="mt-12">
        <p className="text-sm text-text-secondary mb-4">Want early access?</p>
        <Link to="/contact" className="text-accent-blue font-medium hover:underline">Contact our team</Link>
      </div>
    </div>
  );
}
