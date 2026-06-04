interface AssessmentOverviewCardProps {
  overallScore: number;
  rating: string;
  confidenceIndex: number;
  evidenceQuality: number;
}

export function AssessmentOverviewCard({
  overallScore,
  rating,
  confidenceIndex,
  evidenceQuality
}: AssessmentOverviewCardProps) {
  return (
    <div className="border border-border-strong bg-bg-primary mb-12">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-0 text-center md:text-left">
        <div className="p-6 border-b md:border-b-0 md:border-r border-border-light flex flex-col justify-center items-center md:items-start">
          <div className="text-label text-text-secondary mb-1">Overall Score</div>
          <div className="flex items-baseline gap-1">
            <span className="text-h2 font-mono font-bold text-text-primary">{overallScore}</span>
            <span className="text-body text-text-secondary">/100</span>
          </div>
        </div>

        <div className="p-6 border-b md:border-b-0 md:border-r border-border-light flex flex-col justify-center items-center md:items-start">
          <div className="text-label text-text-secondary mb-1">Rating</div>
          <div className="text-h4 font-medium text-text-primary">{rating}</div>
        </div>

        <div className="p-6 border-r border-border-light flex flex-col justify-center items-center md:items-start">
          <div className="text-label text-text-secondary mb-1">Confidence Index</div>
          <div className="flex items-baseline gap-1">
            <span className="text-h4 font-mono font-medium text-text-primary">{confidenceIndex}%</span>
          </div>
        </div>

        <div className="p-6 flex flex-col justify-center items-center md:items-start">
          <div className="text-label text-text-secondary mb-1">Evidence Quality</div>
          <div className="flex items-baseline gap-1">
            <span className="text-h4 font-mono font-medium text-text-primary">{evidenceQuality}/100</span>
          </div>
        </div>
      </div>
    </div>
  );
}
