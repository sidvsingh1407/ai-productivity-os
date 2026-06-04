type SeverityLevel = 'Critical' | 'Major' | 'Moderate' | 'Advisory';

interface SeverityBadgeProps {
  level: SeverityLevel;
}

export function SeverityBadge({ level }: SeverityBadgeProps) {
  const styles = {
    Critical: 'bg-accent-red/10 text-accent-red border-accent-red/20',
    Major: 'bg-accent-amber/10 text-accent-amber border-accent-amber/20',
    Moderate: 'bg-text-primary/10 text-text-primary border-text-primary/20',
    Advisory: 'bg-text-secondary/10 text-text-secondary border-text-secondary/20'
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-none border text-data font-medium ${styles[level]}`}>
      {level}
    </span>
  );
}

interface FindingCardProps {
  number: number;
  title: string;
  severity: SeverityLevel | string;
  impact: string;
  rationale: string;
}

export function FindingCard({ number, title, severity, impact, rationale }: FindingCardProps) {
  // Coerce severity string to SeverityLevel to avoid TS errors or missing styles
  const validSeverity = (['Critical', 'Major', 'Moderate', 'Advisory'].includes(severity as string) ? severity : 'Advisory') as SeverityLevel;

  return (
    <div className={`border-t border-border-light py-6 flex gap-6 ${validSeverity === 'Critical' ? 'bg-accent-red/5 px-6 -mx-6 border-l-4 border-l-accent-red' : ''}`}>
      <div className="text-h3 font-mono text-text-secondary pt-1">
        {String(number).padStart(2, '0')}
      </div>
      <div className="flex-1">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-h3 font-medium text-text-primary">{title}</h3>
          <SeverityBadge level={validSeverity} />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="text-label text-text-secondary uppercase tracking-wider mb-2">Operational Impact</h4>
            <p className="text-body text-text-primary">{impact}</p>
          </div>
          <div>
            <h4 className="text-label text-text-secondary uppercase tracking-wider mb-2">Rationale</h4>
            <p className="text-body text-text-secondary">{rationale}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
