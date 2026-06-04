


interface ExecutiveSummaryCardProps {
  score: number;
  maxScore?: number;
  verdict: string;
  onViewFullReport?: () => void;
  onExportPdf?: () => void;
}

export function ExecutiveSummaryCard({
  score,
  maxScore = 100,
  verdict,
  onViewFullReport,
  onExportPdf
}: ExecutiveSummaryCardProps) {
  return (
    <div className="border border-border-strong bg-bg-primary rounded-none mb-12">
      <div className="p-8 grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="col-span-1 border-r border-border-light pr-8 flex flex-col justify-center">
          <div className="text-label text-text-secondary mb-2">AI Maturity Score</div>
          <div className="flex items-baseline gap-2">
            <span className="text-[64px] font-bold leading-none font-mono text-text-primary">{score}</span>
            <span className="text-h3 font-mono text-text-secondary">/ {maxScore}</span>
          </div>
        </div>
        <div className="col-span-1 md:col-span-3 flex flex-col justify-center">
          <div className="text-label text-text-secondary mb-2">Verdict</div>
          <p className="text-h2 font-medium text-text-primary mb-6">"{verdict}"</p>

          {(onViewFullReport || onExportPdf) && (
            <div className="flex gap-4 mt-auto">
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
      </div>
    </div>
  );
}
