import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { SeoHead } from '../../components/geo/SeoHead';

export default function DpaPage() {
  const navigate = useNavigate();

  return (
    <div className="bg-bg-primary min-h-screen animate-fade-up">
      <SeoHead
        title="Data Processing Agreement | TarkaX"
        description="Data Processing Agreement for the TarkaX platform."
        canonical="https://tarkax.com/dpa"
      />
      <div className="max-w-3xl mx-auto py-24 px-6">
        <h1 className="text-h1 font-semibold mb-8 border-b border-border-light pb-4">Data Processing Agreement (DPA)</h1>

        <div className="bg-bg-secondary p-10 rounded-lg shadow-subtle border border-border-light text-center space-y-6">
          <h2 className="text-h2 font-serif text-text-primary">Legal Review Required</h2>

          <div className="text-body text-text-secondary space-y-4 text-left">
              <p>
                  <strong>Notice:</strong> The Data Processing Agreement (DPA) for this platform is currently a placeholder and requires formal legal review and approval before publication.
              </p>
              <p>
                  This page does not represent a finalized, effective legal agreement or data-processing commitment.
              </p>
          </div>

          <div className="pt-6 border-t border-border-light flex flex-col sm:flex-row gap-4 justify-center">
              <button
                  onClick={() => navigate('/')}
                  className="px-6 py-3 bg-bg-primary border border-border-strong hover:bg-bg-secondary text-text-primary rounded-md transition-colors font-medium"
              >
                  Return Home
              </button>
              <button
                  onClick={() => navigate('/contact')}
                  className="px-6 py-3 bg-accent-blue hover:bg-accent-blue/90 text-text-inverse rounded-md transition-colors font-medium flex items-center justify-center gap-2"
              >
                  Contact Us <ArrowRight className="w-4 h-4" />
              </button>
          </div>
        </div>
      </div>
    </div>
  );
}
