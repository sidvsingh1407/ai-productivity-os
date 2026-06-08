import { SolutionTemplate } from './SolutionTemplate';

export default function ImproveVisibilityPage() {
  return (
    <SolutionTemplate
      title="Improve Operational Visibility"
      seoTitle="Improve Visibility"
      description="Dashboards only show you what happened. TarkaX shows you why it happened and what's fundamentally broken in your operating system."
      benefits={[
        "Move beyond surface-level metrics to understand underlying structural reality.",
        "Bridge the gap between executive perception and operator reality.",
        "Make resource allocation decisions based on empirical evidence, not guessing.",
        "Identify the root causes of failure before they impact the bottom line."
      ]}
      howWeHelp={[
        { step: "Establish a Baseline", detail: "Run comprehensive diagnostic instruments across teams to capture an accurate snapshot of current operations." },
        { step: "Identify Structural Disconnects", detail: "Highlight areas where the intended process and the actual process diverge significantly." },
        { step: "Generate Executive Intelligence", detail: "Translate raw operational data into clear, actionable insights for leadership." },
        { step: "Enable Targeted Interventions", detail: "Provide the exact evidence needed to fix the most critical broken link in the business." }
      ]}
      productLensUrl="/register"
      productLensLabel="Start Free Analysis"
    />
  );
}
