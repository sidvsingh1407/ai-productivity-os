import { ProblemTemplate } from './ProblemTemplate';

export default function OperationsChaoticPage() {
  return (
    <ProblemTemplate
      title="Operations Are Becoming Chaotic"
      seoTitle="Chaotic Operations"
      description="As you scale, the duct tape holding your processes together is starting to fail. Discover the structural weaknesses before things break."
      symptoms={[
        "Customer issues are falling through the cracks.",
        "Every problem requires an 'all hands on deck' fire drill to solve.",
        "Nobody knows exactly how data moves from Sales to Fulfillment.",
        "You rely heavily on massive, fragile spreadsheets."
      ]}
      hiddenCauses={[
        "Processes were built for a 10-person team and haven't evolved for a 50-person team.",
        "Lack of centralized operational visibility—everyone only sees their piece of the puzzle.",
        "Shadow IT—teams are adopting unauthorized tools to solve local problems, breaking global workflows.",
        "No standardized exception handling; edge cases derail the entire system."
      ]}
      findingExample={{
        stat: "4 critical single points of failure identified in fulfillment.",
        description: "If two specific employees are out sick, four core operational processes completely halt because the knowledge is uncodified and access is restricted.",
        impact: "High execution risk and inability to scale team size effectively."
      }}
      productLensUrl="/register"
      productLensLabel="Start Free Analysis"
    />
  );
}
