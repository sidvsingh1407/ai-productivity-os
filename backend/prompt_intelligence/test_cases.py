import json
from prompt_intelligence.context_classifier import ContextClassifier
from prompt_intelligence.diagnosis_engine import DiagnosisEngine

def run_tests():
    test_prompts = {
        "Process Automation": "We need to automate the approval routing for our new SOP. If an exception happens, fallback to the manager. Output the workflow in JSON format. The outcome success metric is zero manual handoffs.",
        "Reporting & Analytics": "Build a dashboard to show KPI metrics and summary trends.",
        "Decision Support": "Evaluate these options and recommend the best strategy. The criteria for decision is budget constraint.",
        "Governance & Compliance": "Review this policy for compliance and audit controls.",
        "Client Diagnostics": "Generate findings and recommendations from this maturity assessment. The audience is the executive team.",
        "Workflow Design": "Create a process map detailing roles, responsibilities, and handoff triggers.",
        "General Operations": "Please rewrite this paragraph so it sounds better."
    }

    for category, prompt in test_prompts.items():
        print("="*60)
        print(f"TESTING CATEGORY: {category}")
        print("-"*60)
        print(f"Prompt: {prompt}")

        # PI-1: Context Classification
        context_result = ContextClassifier.classify(prompt)
        print(f"\n[PI-1] Detected Context: {context_result['context']}")
        print(f"[PI-1] Confidence: {context_result['confidence']}")
        print(f"[PI-1] Reasoning: {json.dumps(context_result['reasoning'])}")

        # PI-2: Operational Diagnosis
        diagnosis_result = DiagnosisEngine.diagnose(prompt)
        print(f"\n[PI-2] Strength: {diagnosis_result['strength']}")
        print(f"[PI-2] Missing Elements: {json.dumps(diagnosis_result['missing_elements'])}")
        print(f"[PI-2] Execution Risks: {json.dumps(diagnosis_result['execution_risks'])}")
        print("\n")

if __name__ == "__main__":
    run_tests()
