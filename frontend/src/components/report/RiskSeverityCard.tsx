import { AlertTriangle, ShieldAlert, Activity } from 'lucide-react';

interface RiskSeverityCardProps {
  riskLevel: string;
  riskScore: number;
  confidence: number;
  topRiskDriver: string;
  projectedImpactSummary: string;
}

export function RiskSeverityCard({
  riskLevel,
  riskScore,
  confidence,
  topRiskDriver,
  projectedImpactSummary
}: RiskSeverityCardProps) {
  return (
    <div className="border border-border-strong bg-bg-primary mb-12">
      <div className="p-8 border-b border-border-light bg-bg-secondary flex justify-between items-start">
        <div>
          <h2 className="text-h2 font-semibold text-text-primary mb-2">Current Risk Profile</h2>
          <p className="text-body text-text-secondary">
            Evaluation of near-term exposure based on identified maturity gaps.
          </p>
        </div>
        <div className="flex flex-col items-end">
          <span className="text-label text-text-secondary uppercase mb-1">Overall Risk Level</span>
          <span className={`text-h2 font-semibold ${riskLevel === 'Critical' ? 'text-accent-red' : riskLevel === 'High' ? 'text-accent-red/80' : 'text-text-primary'}`}>
            {riskLevel}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-0">
        <div className="p-6 border-b md:border-b-0 md:border-r border-border-light flex flex-col gap-3">
          <div className="flex items-center gap-2 text-text-primary font-medium">
            <Activity className="w-5 h-5 text-text-secondary" />
            <span className="text-label uppercase tracking-wider">Confidence Index</span>
          </div>
          <p className="text-h3 font-medium text-text-primary">{confidence}%</p>
          <p className="text-sm text-text-secondary">Based on data consistency</p>
        </div>

        <div className="p-6 md:col-span-2 flex flex-col gap-3">
          <div className="flex items-center gap-2 text-text-primary font-medium">
            <AlertTriangle className="w-5 h-5 text-text-secondary" />
            <span className="text-label uppercase tracking-wider">Primary Risk Driver</span>
          </div>
          <p className="text-body font-medium text-text-primary">{topRiskDriver}</p>
        </div>
      </div>

      <div className="p-8 border-t border-border-light bg-text-primary/5">
        <h3 className="text-label text-text-secondary uppercase tracking-wider mb-4">Projected Business Impact Summary</h3>
        <p className="text-body text-text-primary leading-relaxed max-w-4xl font-medium">
          {projectedImpactSummary}
        </p>
      </div>
    </div>
  );
}
