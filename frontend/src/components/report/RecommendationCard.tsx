import React from 'react';

interface RecommendationCardProps {
  number: number;
  action: string;
  rationale: string;
  futureState: string;
}

export function RecommendationCard({ number, action, rationale, futureState }: RecommendationCardProps) {
  return (
    <div className="border border-border-strong bg-bg-primary p-6 mb-6">
      <div className="flex gap-4 items-start mb-4">
        <div className="w-8 h-8 bg-text-primary text-text-inverse flex items-center justify-center font-mono text-data">
          {number}
        </div>
        <h3 className="text-h3 font-medium text-text-primary pt-0.5">{action}</h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 ml-12">
        <div>
          <div className="text-label text-text-secondary mb-2">Rationale</div>
          <p className="text-body text-text-secondary">{rationale}</p>
        </div>
        <div>
          <div className="text-label text-text-secondary mb-2">Desired Future State</div>
          <p className="text-body text-text-secondary">{futureState}</p>
        </div>
      </div>
    </div>
  );
}
