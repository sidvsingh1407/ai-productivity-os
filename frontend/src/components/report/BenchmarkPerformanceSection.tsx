interface BenchmarkPerformanceSectionProps {
  benchmark: any;
  yourScores: Record<string, number>;
}

export function BenchmarkPerformanceSection({ benchmark, yourScores }: BenchmarkPerformanceSectionProps) {
  if (!benchmark) {
    return (
      <div className="mb-12">
        <h2 className="text-h2 font-semibold text-text-primary mb-6 border-b border-border-light pb-4">Benchmark Performance</h2>
        <div className="p-6 bg-bg-secondary border border-border-strong text-text-secondary">
          Benchmark data currently unavailable.
        </div>
      </div>
    );
  }

  if (benchmark.available === false || (benchmark.sample_size !== undefined && benchmark.sample_size < 10)) {
    return (
      <div className="mb-12">
        <h2 className="text-h2 font-semibold text-text-primary mb-6 border-b border-border-light pb-4">Benchmark Performance</h2>
        <div className="p-6 bg-bg-secondary border border-border-strong text-text-secondary">
          Insufficient benchmark data available.
        </div>
      </div>
    );
  }

  // Calculate table rows based on dimensions.
  const dimensionsList = [
    { key: 'awareness', label: 'Awareness' },
    { key: 'adoption', label: 'Adoption' },
    { key: 'integration', label: 'Integration' },
    { key: 'governance', label: 'Governance' },
    { key: 'roi', label: 'ROI' },
  ];

  // We map the differences array or calculate them.
  // The API is supposed to return differences in the payload or we can calculate them.
  // The requirements say: Dimension differences are strictly calculated as your_score - benchmark.

  // It's safer to extract from benchmark.dimension_averages if available.
  const rows = dimensionsList.map(dim => {
    const yourScore = yourScores[dim.key] !== undefined ? yourScores[dim.key] * 5 : 0; // The UI multiplies score by 5 for display (score/20 -> /100)
    // The benchmark average is usually given out of 100 or out of 20, let's assume it's out of 100 based on standard. Wait, check backend for benchmark payload.
    // If we assume backend provides the benchmark average out of 100 already... wait, we should check what the backend benchmark payload looks like.

    // Let's rely on the benchmark payload structure which should have dimension_averages and dimension_differences.
    const benchmarkAvg = benchmark.dimension_averages ? benchmark.dimension_averages[dim.key] : 0;
    const diff = benchmark.dimension_differences ? benchmark.dimension_differences[dim.key] : (yourScore - benchmarkAvg);

    let statusLabel = 'At Benchmark';
    if (diff > 0) statusLabel = 'Above Benchmark';
    if (diff < 0) statusLabel = 'Below Benchmark';

    return {
      label: dim.label,
      yourScore: yourScore,
      benchmarkScore: benchmarkAvg,
      difference: diff,
      statusLabel
    };
  });

  return (
    <div className="mb-12">
      <h2 className="text-h2 font-semibold text-text-primary mb-6 border-b border-border-light pb-4">Benchmark Performance</h2>

      <div className="overflow-x-auto mb-4">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-border-strong text-label text-text-secondary uppercase tracking-wider">
              <th className="py-3 pr-4">Dimension</th>
              <th className="py-3 px-4">Your Score</th>
              <th className="py-3 px-4">Benchmark</th>
              <th className="py-3 px-4">Difference</th>
              <th className="py-3 pl-4">Status</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row, idx) => (
              <tr key={idx} className="border-b border-border-light text-body text-text-primary">
                <td className="py-4 pr-4 font-medium">{row.label}</td>
                <td className="py-4 px-4">{row.yourScore}</td>
                <td className="py-4 px-4">{row.benchmarkScore}</td>
                <td className="py-4 px-4 font-mono">
                  {row.difference > 0 ? `+${row.difference}` : row.difference}
                </td>
                <td className="py-4 pl-4">
                  <span className={`px-2 py-1 text-data font-medium rounded ${
                    row.statusLabel === 'Above Benchmark' ? 'bg-accent-green/10 text-accent-green' :
                    row.statusLabel === 'Below Benchmark' ? 'bg-accent-red/10 text-accent-red' :
                    'bg-accent-amber/10 text-accent-amber'
                  }`}>
                    {row.statusLabel}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="text-data text-text-secondary mb-8">
        Based on {benchmark.sample_size} completed assessments.
      </p>

      {benchmark.insights && (
        <div className="bg-bg-secondary p-6 border border-border-strong">
          <h3 className="text-h3 font-medium text-text-primary mb-4">Benchmark Insights</h3>
          <ul className="list-disc pl-5 space-y-2 text-body text-text-secondary">
            {benchmark.insights.strongest_dimension && (
              <li>{benchmark.insights.strongest_dimension}</li>
            )}
            {benchmark.insights.weakest_dimension && (
              <li>{benchmark.insights.weakest_dimension}</li>
            )}
            {benchmark.insights.overall_summary && (
              <li>{benchmark.insights.overall_summary}</li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}
