import { SolutionTemplate } from './SolutionTemplate';

export default function ReduceManualWorkPage() {
  return (
    <SolutionTemplate
      title="Reduce Manual Work"
      seoTitle="Reduce Manual Work"
      description="Your highly-paid experts shouldn't be doing data entry. TarkaX identifies repetitive manual tasks so you know exactly what to automate next."
      benefits={[
        "Identify the 'glue work' happening in spreadsheets and emails.",
        "Quantify the exact hours lost to redundant data entry.",
        "Protect employee morale by eliminating mind-numbing administrative tasks.",
        "Create a prioritized backlog of high-ROI automation targets."
      ]}
      howWeHelp={[
        { step: "Survey Operational Reality", detail: "Capture data directly from operators to find the tasks that aren't documented in the official playbook." },
        { step: "Map Tool Disconnects", detail: "Identify where systems fail to talk to each other, forcing humans to act as the integration layer." },
        { step: "Calculate the Waste", detail: "Aggregate the hidden minutes spent copying and pasting to reveal the massive organizational cost." },
        { step: "Recommend Automation Paths", detail: "Provide clear evidence of which manual tasks should be eliminated, delegated, or automated." }
      ]}
      productLensUrl="/register"
      productLensLabel="Run Workflow Diagnostic"
    />
  );
}
