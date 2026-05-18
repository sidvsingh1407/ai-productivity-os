import React from 'react';
import { useModalStore } from '@/store/modalStore';
import { useNavigate } from 'react-router-dom';
import { Activity, ShieldCheck } from 'lucide-react';

export const LandingPage: React.FC = () => {
  const { hasAcknowledgedNotice, openModal } = useModalStore();
  const navigate = useNavigate();

  const handleAction = (route: string) => {
    if (hasAcknowledgedNotice) {
      navigate(route);
    } else {
      openModal(route);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <main className="relative flex items-center justify-center min-h-screen px-4 sm:px-6 lg:px-8 overflow-hidden">

        {/* Abstract cinematic background elements */}
        <div className="absolute inset-0 pointer-events-none overflow-hidden">
          <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-tarkha-teal/5 blur-[120px] rounded-full" />
          <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-tarkha-gold/5 blur-[120px] rounded-full" />
        </div>

        <div className="relative z-10 max-w-4xl mx-auto text-center space-y-10">
          <div className="space-y-4">
            <h1 className="text-4xl sm:text-6xl md:text-7xl font-serif text-gray-900 tracking-tight leading-tight">
              Executive Intelligence.<br />
              <span className="text-tarkha-gold">Operational Excellence.</span>
            </h1>
            <p className="max-w-2xl mx-auto text-lg sm:text-xl text-gray-600 font-sans leading-relaxed">
              TarkhaX provides AI-assisted operational analysis, workflow diagnostics, and maturity assessments for strategic enterprise optimization.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <button
              onClick={() => handleAction('/audits/new')}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 bg-gray-900 hover:bg-gray-800 text-white font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-2"
            >
              <ShieldCheck className="w-5 h-5 text-tarkha-emerald" />
              Run AI Audit
            </button>
            <button
              onClick={() => handleAction('/workflows/new')}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 bg-white border border-gray-200 hover:border-tarkha-gold/50 hover:bg-gray-50 text-gray-900 font-medium rounded-md transition-all focus:outline-none focus:ring-2 focus:ring-gray-200 focus:ring-offset-2 shadow-sm"
            >
              <Activity className="w-5 h-5 text-tarkha-teal" />
              Explore Workflow Diagnosis
            </button>
          </div>
        </div>
      </main>
    </div>
  );
};
