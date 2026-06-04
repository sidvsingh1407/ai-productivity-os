

interface ScoreBreakdownProps {
  dimensions: Array<{
    label: string;
    score: number;
    keyFinding: string;
  }>;
}

export function ScoreBreakdown({ dimensions }: ScoreBreakdownProps) {
  const getScoreColor = (score: number) => {
    if (score > 75) return 'bg-accent-green';
    if (score >= 50) return 'bg-accent-amber';
    return 'bg-accent-red';
  };

  const getScoreLabel = (score: number) => {
    if (score > 75) return 'Mature';
    if (score >= 50) return 'Developing';
    return 'Critical';
  };

  return (
    <div className="mb-12">
      <h2 className="text-h2 font-semibold text-text-primary mb-6 border-b border-border-light pb-4">Dimension Breakdown</h2>
      <div className="space-y-6">
        {dimensions.map((dim, idx) => (
          <div key={idx} className="grid grid-cols-1 md:grid-cols-12 gap-6 items-start">
            <div className="md:col-span-3">
              <div className="text-h3 font-medium text-text-primary">{dim.label}</div>
              <div className="text-data text-text-secondary mt-1">{dim.score} / 100 — {getScoreLabel(dim.score)}</div>
            </div>
            <div className="md:col-span-4 pt-2">
              <div className="w-full h-3 bg-bg-secondary rounded-none overflow-hidden border border-border-light">
                <div
                  className={`h-full ${getScoreColor(dim.score)}`}
                  style={{ width: `${Math.max(0, Math.min(100, dim.score))}%` }}
                />
              </div>
            </div>
            <div className="md:col-span-5">
              <p className="text-body text-text-secondary border-l-2 border-border-strong pl-4">
                {dim.keyFinding}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
