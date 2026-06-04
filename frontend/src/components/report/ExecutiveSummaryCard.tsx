import { ShieldAlert, TrendingUp, CheckCircle2 } from 'lucide-react';

interface ExecutiveSummaryCardProps {
  overallAssessment: string;
  criticalRisk: string;
  biggestOpportunity: string;
  recommendedFirstAction: string;
  onViewFullReport?: () => void;
  onExportPdf?: () => void;
}

export function ExecutiveSummaryCard({
  overallAssessment,
  criticalRisk,
  biggestOpportunity,
  recommendedFirstAction,
  onViewFullReport,
  onExportPdf
}: ExecutiveSummaryCardProps) {
  return (
    <div className="border border-border-strong bg-bg-primary mb-12">
      <div className="p-8 border-b border-border-light bg-bg-secondary">
        <h2 className="text-h2 font-semibold text-text-primary mb-2">Executive Summary</h2>
        <p className="text-body text-text-secondary leading-relaxed max-w-4xl">
          {overallAssessment}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-0">
        <div className="p-6 border-b md:border-b-0 md:border-r border-border-light flex flex-col gap-3">
          <div className="flex items-center gap-2 text-accent-red font-medium">
            <ShieldAlert className="w-5 h-5" />
            <span className="text-label uppercase tracking-wider">Most Critical Risk</span>
          </div>
          <p className="text-body font-medium text-text-primary">{criticalRisk}</p>
        </div>

        <div className="p-6 border-b md:border-b-0 md:border-r border-border-light flex flex-col gap-3">
          <div className="flex items-center gap-2 text-text-primary font-medium">
            <TrendingUp className="w-5 h-5" />
            <span className="text-label uppercase tracking-wider">Biggest Opportunity</span>
          </div>
          <p className="text-body font-medium text-text-primary">{biggestOpportunity}</p>
        </div>

        <div className="p-6 flex flex-col gap-3 bg-text-primary/5">
          <div className="flex items-center gap-2 text-text-primary font-medium">
            <CheckCircle2 className="w-5 h-5" />
            <span className="text-label uppercase tracking-wider">Recommended First Action</span>
          </div>
          <p className="text-body font-medium text-text-primary">{recommendedFirstAction}</p>
        </div>
      </div>

      {(onViewFullReport || onExportPdf) && (
        <div className="p-6 border-t border-border-light flex gap-4 bg-bg-secondary justify-end">
          {onViewFullReport && (
            <button
              onClick={onViewFullReport}
              className="px-6 py-3 bg-text-primary text-text-inverse text-body font-medium transition-colors hover:bg-text-primary/90"
            >
              View Full Report
            </button>
          )}
          {onExportPdf && (
            <button
              onClick={onExportPdf}
              className="px-6 py-3 bg-bg-primary border border-border-strong text-text-primary text-body font-medium transition-colors hover:bg-bg-secondary"
            >
              Export PDF
            </button>
          )}
        </div>
      )}
    </div>
  );
}
