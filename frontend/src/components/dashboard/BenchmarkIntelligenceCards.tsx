interface BenchmarkIntelligenceCardsProps {
  benchmark: any;
}

export function BenchmarkIntelligenceCards({ benchmark }: BenchmarkIntelligenceCardsProps) {
  if (!benchmark) {
    return (
      <div className="mb-12">
        <h2 className="text-h2 font-semibold text-text-primary mb-6 border-b border-border-light pb-4">Benchmark Intelligence</h2>
        <div className="p-6 bg-bg-secondary border border-border-strong text-text-secondary">
          Benchmark data currently unavailable.
        </div>
      </div>
    );
  }

  if (benchmark.available === false || (benchmark.sample_size !== undefined && benchmark.sample_size < 10)) {
    return (
      <div className="mb-12">
        <h2 className="text-h2 font-semibold text-text-primary mb-6 border-b border-border-light pb-4">Benchmark Intelligence</h2>
        <div className="p-6 bg-bg-secondary border border-border-strong text-text-secondary">
          Insufficient benchmark data available.
        </div>
      </div>
    );
  }

  // Card values based on insights.
  // Actually, strongest and weakest dimensions could be extracted more safely if the backend payload returns a specific format.
  // The backend might return "Governance exceeds the platform average by 12 points." inside strongest_dimension string.
  // But we want to display Card Title: "Governance", Card Value: "+12 vs Benchmark" or similar according to requirements.
  // Let's assume we can compute strongest and weakest from dimension_differences if needed, or if insights have structured data.
  // We'll compute them manually from `dimension_differences` just to be sure we format exactly as requested: "Governance", "+12 vs Benchmark".

  let strongestName = 'N/A';
  let strongestValue = '+0 vs Benchmark';
  let weakestName = 'N/A';
  let weakestValue = '-0 vs Benchmark';
  let positiveCount = 0;

  if (benchmark.dimension_differences) {
    const diffs = benchmark.dimension_differences;
    let maxDiff = -Infinity;
    let minDiff = Infinity;

    // According to TarkaX logic, dimensions to check are: awareness, adoption, integration, governance, roi
    const dims = ['awareness', 'adoption', 'integration', 'governance', 'roi'];

    for (const key of dims) {
      if (diffs[key] !== undefined) {
        const val = diffs[key];
        if (val > 0) positiveCount++;

        if (val > maxDiff) {
          maxDiff = val;
          strongestName = key.charAt(0).toUpperCase() + key.slice(1);
          strongestValue = `${val > 0 ? '+' : ''}${val} vs Benchmark`;
        }
        if (val < minDiff) {
          minDiff = val;
          weakestName = key.charAt(0).toUpperCase() + key.slice(1);
          weakestValue = `${val > 0 ? '+' : ''}${val} vs Benchmark`;
        }
      }
    }
  }

  const relativeSummary = `Your organization performs above the benchmark in ${positiveCount} of 5 dimensions.`;

  return (
    <div className="mb-12">
      <h2 className="text-h2 font-semibold text-text-primary mb-6 border-b border-border-light pb-4">Benchmark Intelligence</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Card 1: Overall Benchmark Position */}
        <div className="border border-border-strong bg-bg-primary p-6">
          <h3 className="text-label text-text-secondary mb-2 uppercase tracking-wider">Overall Benchmark Position</h3>
          <h2 className="text-h2 text-text-primary">{benchmark.percentile ? `Top ${100 - benchmark.percentile}%` : 'Above Platform Average'}</h2>
        </div>

        {/* Card 2: Strongest Dimension */}
        <div className="border border-border-strong bg-bg-primary p-6">
          <h3 className="text-label text-text-secondary mb-2 uppercase tracking-wider">Strongest Dimension</h3>
          <h2 className="text-h2 text-text-primary mb-1">{strongestName}</h2>
          <p className="text-body font-medium text-accent-green">{strongestValue}</p>
        </div>

        {/* Card 3: Weakest Dimension */}
        <div className="border border-border-strong bg-bg-primary p-6">
          <h3 className="text-label text-text-secondary mb-2 uppercase tracking-wider">Weakest Dimension</h3>
          <h2 className="text-h2 text-text-primary mb-1">{weakestName}</h2>
          <p className="text-body font-medium text-accent-red">{weakestValue}</p>
        </div>

        {/* Card 4: Relative Performance Summary */}
        <div className="border border-border-strong bg-bg-primary p-6">
          <h3 className="text-label text-text-secondary mb-2 uppercase tracking-wider">Relative Performance Summary</h3>
          <p className="text-body text-text-primary mt-1">{relativeSummary}</p>
        </div>
      </div>

      <p className="text-data text-text-secondary mt-4">
        Based on {benchmark.sample_size} completed assessments.
      </p>
    </div>
  );
}
