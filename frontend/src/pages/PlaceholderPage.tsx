import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';

export const PlaceholderPage: React.FC<{ title: string }> = ({ title }) => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-bg-primary p-6">
      <div className="max-w-xl w-full bg-bg-secondary p-10 rounded-lg shadow-subtle border border-border-light text-center space-y-6">
        <h1 className="text-h2 font-serif text-text-primary">{title} Capability Coming Soon</h1>

        <div className="text-body text-text-secondary space-y-4 text-left">
            <p>
                <strong>What this is:</strong> This capability is currently under active development. It will provide advanced operational intelligence and observability for your organization.
            </p>
            <p>
                <strong>Why it exists:</strong> TarkaX is building this module to bridge the gap between operational noise and actionable structural reality, allowing leadership to make evidence-based interventions.
            </p>
            <p>
                <strong>Future Purpose:</strong> Once released, this module will integrate directly into your existing decision support interface, expanding your diagnostic tools.
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
                Contact for Early Access <ArrowRight className="w-4 h-4" />
            </button>
        </div>
      </div>
    </div>
  );
};
