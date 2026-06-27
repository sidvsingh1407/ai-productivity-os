import { ProblemTemplate } from './ProblemTemplate';

export default function TeamProductivityPage() {
  return (
    <ProblemTemplate
      title="Team Productivity Is Stalling"
      seoTitle="Stalling Team Productivity"
      description="Despite new hires and new software, things are moving slower than ever. Discover the hidden friction dragging down your team's output."
      symptoms={[
        "Projects constantly get stuck in review or approval stages.",
        "Team members complain about being overwhelmed by administrative tasks.",
        "It takes longer to do simple things than it did a year ago.",
        "Information is scattered across Slack, email, and outdated wikis."
      ]}
      hiddenCauses={[
        "Unclear decision rights cause unnecessary handoffs and meetings.",
        "Tool bloat has fragmented workflows, requiring constant context switching.",
        "Core processes exist only in people's heads, creating single points of failure.",
        "Manual data entry bridges the gaps between disconnected software platforms."
      ]}
      findingExample={{
        stat: "14-hour delay in standard approval loop.",
        description: "Client onboarding requires a manual PDF review by compliance. Because the handoff relies on email rather than an automated queue, requests sit unseen for an average of 14 hours.",
        impact: "Reduced client satisfaction and delayed revenue recognition."
      }}
      productLensUrl="/register"
      productLensLabel="Run Workflow Intelligence"
    />
  );
}
