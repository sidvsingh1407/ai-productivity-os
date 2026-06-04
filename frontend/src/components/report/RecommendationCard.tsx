interface RecommendationCardProps {
  number: number;
  recommendation: string;
  priority: string;
  expectedImpact: string;
  implementationEffort: string;
}

export function RecommendationCard({
  number,
  recommendation,
  priority,
  expectedImpact,
  implementationEffort
}: RecommendationCardProps) {
  return (
    <div className="border border-border-strong bg-bg-primary p-6 mb-6">
      <div className="flex flex-col md:flex-row md:items-start justify-between gap-4 mb-6">
        <div className="flex gap-4 items-start">
          <div className="w-8 h-8 bg-text-primary text-text-inverse flex items-center justify-center font-mono text-data shrink-0">
            {number}
          </div>
          <h3 className="text-h3 font-medium text-text-primary pt-0.5">{recommendation}</h3>
        </div>
        <span className={`inline-flex items-center px-3 py-1 rounded-none border text-xs font-medium tracking-wider uppercase whitespace-nowrap ${
          priority.toLowerCase() === 'immediate' ? 'bg-text-primary/10 text-text-primary border-text-primary/20' :
          priority.toLowerCase() === 'near-term' ? 'bg-bg-secondary text-text-primary border-border-strong' :
          'bg-bg-primary text-text-secondary border-border-light'
        }`}>
          {priority} Priority
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 ml-12">
        <div>
          <div className="text-label text-text-secondary uppercase tracking-wider mb-2">Expected Impact</div>
          <p className="text-body text-text-primary">{expectedImpact}</p>
        </div>
        <div>
          <div className="text-label text-text-secondary uppercase tracking-wider mb-2">Implementation Effort</div>
          <p className="text-body text-text-secondary">{implementationEffort}</p>
        </div>
      </div>
    </div>
  );
}
