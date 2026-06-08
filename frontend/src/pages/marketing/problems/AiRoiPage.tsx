import { ProblemTemplate } from './ProblemTemplate';

export default function AiRoiPage() {
  return (
    <ProblemTemplate
      title="AI Isn't Delivering ROI"
      seoTitle="AI ROI Problems"
      description="You bought the licenses and ran the pilots, but the promised productivity gains haven't materialized. Discover where your AI investments are leaking value."
      symptoms={[
        "Employees are returning to old, manual ways of working.",
        "Execs see the bill, but can't see the business impact.",
        "AI output requires too much human review to be useful.",
        "Only a small handful of 'power users' are actively using the tools."
      ]}
      hiddenCauses={[
        "Lack of clear operational guidelines means employees are afraid of making mistakes.",
        "Tools were deployed generally, instead of targeted at specific bottlenecks.",
        "Prompts are inconsistent and undocumented, leading to unpredictable quality.",
        "Data silos prevent AI tools from accessing the context they need to be useful."
      ]}
      findingExample={{
        stat: "73% of AI licenses unused or underutilized.",
        description: "Licenses were purchased for 100 employees across three departments, but only 27 are using them more than once a week. The rest abandoned the tools after initial onboarding.",
        impact: "$18,000 annual waste and 0% productivity gain in core workflows."
      }}
      productLensUrl="/register"
      productLensLabel="Run AI Audit"
    />
  );
}
