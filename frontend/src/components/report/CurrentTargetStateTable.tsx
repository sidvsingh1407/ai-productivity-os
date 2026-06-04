interface TargetStateItem {
  dimension: string;
  current_score: number;
  target_score: number;
  gap: number;
  improvement_priority: string;
  rationale: string;
}

interface CurrentTargetStateTableProps {
  targetState: TargetStateItem[];
}

export function CurrentTargetStateTable({ targetState }: CurrentTargetStateTableProps) {
  if (!targetState || targetState.length === 0) {
    return null;
  }

  return (
    <div className="mb-12">
      <h2 className="text-h2 font-semibold text-text-primary mb-6 border-b border-border-light pb-4">Current vs. Target State</h2>
      <div className="overflow-x-auto border border-border-strong bg-bg-primary">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-bg-secondary border-b border-border-strong">
              <th className="p-4 text-label text-text-secondary uppercase tracking-wider font-medium">Dimension</th>
              <th className="p-4 text-label text-text-secondary uppercase tracking-wider font-medium text-center">Current Score</th>
              <th className="p-4 text-label text-text-secondary uppercase tracking-wider font-medium text-center">Target Score</th>
              <th className="p-4 text-label text-text-secondary uppercase tracking-wider font-medium text-center">Gap</th>
              <th className="p-4 text-label text-text-secondary uppercase tracking-wider font-medium text-center">Priority</th>
              <th className="p-4 text-label text-text-secondary uppercase tracking-wider font-medium">Rationale</th>
            </tr>
          </thead>
          <tbody className="text-body text-text-primary">
            {targetState.map((item, idx) => (
              <tr key={idx} className="border-b border-border-light last:border-b-0 hover:bg-bg-secondary/50 transition-colors">
                <td className="p-4 font-medium">{item.dimension}</td>
                <td className="p-4 font-mono text-center">{item.current_score}</td>
                <td className="p-4 font-mono text-center">{item.target_score}</td>
                <td className="p-4 font-mono text-center text-text-secondary">+{item.gap}</td>
                <td className="p-4 text-center">
                  <span className={`px-2 py-1 text-xs font-medium uppercase tracking-wider ${
                    item.improvement_priority.toLowerCase() === 'high' ? 'bg-accent-red/10 text-accent-red' :
                    item.improvement_priority.toLowerCase() === 'medium' ? 'bg-text-primary/10 text-text-primary' :
                    'bg-bg-secondary text-text-secondary border border-border-strong'
                  }`}>
                    {item.improvement_priority}
                  </span>
                </td>
                <td className="p-4 text-text-secondary text-sm leading-relaxed min-w-[250px]">{item.rationale}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
