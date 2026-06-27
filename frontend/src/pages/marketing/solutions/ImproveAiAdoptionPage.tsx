import { SolutionTemplate } from './SolutionTemplate';

export default function ImproveAiAdoptionPage() {
  return (
    <SolutionTemplate
      title="Improve AI Adoption"
      seoTitle="Improve AI Adoption"
      description="Ensure your AI investments are actually being used. TarkaX evaluates your organizational readiness and uncovers the structural barriers preventing true adoption."
      benefits={[
        "Identify which departments are ready for AI and which require foundational work.",
        "Discover why employees are abandoning AI tools after initial onboarding.",
        "Uncover governance and compliance fears that are secretly blocking usage.",
        "Ensure training and enablement are targeted at the actual skill gaps."
      ]}
      howWeHelp={[
        { step: "Evaluate Readiness", detail: "Our Compliance Readiness measures your organization across five pillars: Awareness, Adoption, Integration, ROI, and Governance." },
        { step: "Identify Structural Barriers", detail: "We look past 'lack of training' to find the real issues: missing guidelines, fear of making mistakes, or disconnected data." },
        { step: "Highlight Utilization Gaps", detail: "See exactly where expensive licenses are sitting idle and the operational reasons why." },
        { step: "Draft an Adoption Roadmap", detail: "Get a clear plan to remove the specific friction points stopping your team from leveraging AI." }
      ]}
      productLensUrl="/register"
      productLensLabel="Run Compliance Readiness"
    />
  );
}
