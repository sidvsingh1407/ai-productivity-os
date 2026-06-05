import { Clock } from 'lucide-react';

interface RiskTimelineProps {
  timeline: {
    near_term: string[];
    mid_term: string[];
    long_term: string[];
  };
}

export function RiskTimeline({ timeline }: RiskTimelineProps) {
  const timeframes = [
    { label: "Current State", icon: <Clock className="w-4 h-4" />, items: ["Maturity gaps identified across core operational dimensions."] },
    { label: "30 Days", icon: <Clock className="w-4 h-4" />, items: timeline.near_term.length > 0 ? timeline.near_term : ["Initial operational friction increases."] },
    { label: "60 Days", icon: <Clock className="w-4 h-4" />, items: timeline.mid_term.length > 0 ? timeline.mid_term : ["Maturity gaps begin affecting execution quality."] },
    { label: "90 Days", icon: <Clock className="w-4 h-4" />, items: timeline.long_term.length > 0 ? timeline.long_term : ["Systemic risks impact strategic outcomes."] },
  ];

  return (
    <div className="mb-12">
      <h2 className="text-h2 font-semibold text-text-primary mb-6 border-b border-border-light pb-4">Risk Progression Timeline</h2>
      <p className="text-body text-text-secondary mb-8 max-w-3xl">
        Expected progression of operational and governance exposure if identified maturity gaps are not addressed.
      </p>

      <div className="relative border-l border-border-strong ml-4 space-y-8 pb-4">
        {timeframes.map((tf, idx) => (
          <div key={idx} className="relative pl-8">
            <div className="absolute -left-3 top-1 w-6 h-6 rounded-full bg-bg-secondary border-2 border-border-strong flex items-center justify-center text-text-secondary">
              <div className="w-2 h-2 rounded-full bg-text-primary"></div>
            </div>
            <div className="mb-2 flex items-center gap-2">
              <span className="text-label text-text-secondary uppercase tracking-wider">{tf.label}</span>
            </div>
            <div className="space-y-2">
              {tf.items.map((item, itemIdx) => (
                <p key={itemIdx} className="text-body text-text-primary font-medium">
                  {item}
                </p>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
