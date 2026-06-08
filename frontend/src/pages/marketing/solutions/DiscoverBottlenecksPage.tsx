import { SolutionTemplate } from './SolutionTemplate';

export default function DiscoverBottlenecksPage() {
  return (
    <SolutionTemplate
      title="Discover Hidden Bottlenecks"
      seoTitle="Discover Bottlenecks"
      description="Stop guessing why projects are delayed. TarkaX maps your actual workflows to reveal the specific handoffs, approvals, and manual tasks dragging down your team."
      benefits={[
        "Pinpoint exactly where processes stall and calculate the cost of the delay.",
        "Identify single points of failure before they become critical emergencies.",
        "Differentiate between software problems and organizational structure problems.",
        "Gain the evidence needed to justify automation investments or process changes."
      ]}
      howWeHelp={[
        { step: "Deploy the Diagnostic", detail: "Send our rapid workflow assessment to the individuals executing the work, not just the managers overseeing it." },
        { step: "Map the Reality", detail: "TarkaX connects the dots, visualizing the hidden steps, workarounds, and shadow IT that make up the real process." },
        { step: "Quantify the Impact", detail: "Every bottleneck is ranked by business impact, showing you the exact cost in hours and dollars." },
        { step: "Provide Targeted Recommendations", detail: "Receive specific, actionable steps to resolve the friction—whether it's changing a rule, automating a handoff, or retraining a team." }
      ]}
      productLensUrl="/register"
      productLensLabel="Run Workflow Diagnostic"
    />
  );
}
