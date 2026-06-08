import { SolutionTemplate } from './SolutionTemplate';

export default function StandardizeAiOutputsPage() {
  return (
    <SolutionTemplate
      title="Standardize AI Outputs"
      seoTitle="Standardize AI Outputs"
      description="Stop crossing your fingers every time your team uses AI. TarkaX analyzes and standardizes prompt structures to guarantee reliable, high-quality outputs."
      benefits={[
        "Eliminate off-brand, generic, or hallucinated responses from AI tools.",
        "Reduce the time employees spend repeatedly editing and re-prompting.",
        "Establish a centralized standard for what a 'good' prompt looks like.",
        "Lower compliance and brand risks associated with unmonitored AI usage."
      ]}
      howWeHelp={[
        { step: "Analyze Existing Prompts", detail: "Review the current prompts your team is using to identify structural weaknesses and missing context." },
        { step: "Score Across 6 Dimensions", detail: "Evaluate prompts for Clarity, Structure, Output Requirements, Operational Usability, Exception Handling, and Decision Criteria." },
        { step: "Generate Optimized Templates", detail: "TarkaX's deterministic engine rewrites the prompts to ensure consistency and reliability." },
        { step: "Deploy Organizational Standards", detail: "Roll out the standardized prompts to the team, replacing ad-hoc 'chatting' with structured engineering." }
      ]}
      productLensUrl="/app/prompt-improver"
      productLensLabel="Try Prompt Improver"
    />
  );
}
