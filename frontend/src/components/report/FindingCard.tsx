import React from 'react';

type SeverityLevel = 'Critical' | 'Major' | 'Advisory';

interface SeverityBadgeProps {
  level: SeverityLevel;
}

export function SeverityBadge({ level }: SeverityBadgeProps) {
  const styles = {
    Critical: 'bg-accent-red/10 text-accent-red border-accent-red/20',
    Major: 'bg-accent-amber/10 text-accent-amber border-accent-amber/20',
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
  explanation: string;
  severity: SeverityLevel;
}

export function FindingCard({ number, title, explanation, severity }: FindingCardProps) {
  return (
    <div className="border-t border-border-light py-6 flex gap-6">
      <div className="text-h3 font-mono text-text-secondary pt-1">
        {String(number).padStart(2, '0')}
      </div>
      <div className="flex-1">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-h3 font-medium text-text-primary">{title}</h3>
          <SeverityBadge level={severity} />
        </div>
        <p className="text-body text-text-secondary">{explanation}</p>
      </div>
    </div>
  );
}
