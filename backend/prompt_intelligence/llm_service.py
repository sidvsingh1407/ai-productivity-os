class LLMService:
    """
    Minimal LLMService abstraction for Prompt Improver.
    In this sprint, it returns deterministic template-generated rewrites
    based on the provided prompts (without external API calls).
    """

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        # In a real scenario, this would call an LLM API.
        # Here we mock the behavior by matching keywords in the user_prompt (which will contain original prompt, context, risks)
        # to generate a structured, deterministic output.

        user_prompt_lower = user_prompt.lower()

        # Extract context if provided in user_prompt
        context = "General Operations"
        if "process automation" in user_prompt_lower:
            context = "Process Automation"
        elif "reporting and analytics" in user_prompt_lower or "reporting & analytics" in user_prompt_lower:
            context = "Reporting and Analytics"
        elif "decision support" in user_prompt_lower:
            context = "Decision Support"
        elif "workflow design" in user_prompt_lower:
            context = "Workflow Design"

        # Generate output based on context
        improved_prompt = f"Objective: To effectively execute tasks within {context}.\n\n"
        improved_prompt += f"Context: This task is related to {context}. Consider standard operational constraints.\n\n"

        # Add context-specific operational indicators and structure
        if context == "Process Automation":
            improved_prompt += "Tasks: Identify manual steps, design approval workflows, and set up automated triggers.\n\n"
            improved_prompt += "Output Expectations: Provide actionable steps, owners, and trigger definitions in JSON format.\n\n"
            improved_prompt += "Success Criteria: The workflow must reduce manual steps by 50%.\n"
        elif context == "Reporting and Analytics":
            improved_prompt += "Tasks: Aggregate data, analyze trends, and present key metrics.\n\n"
            improved_prompt += "Output Expectations: Generate findings, key insights, and priority recommendations in a structured report format.\n\n"
            improved_prompt += "Success Criteria: The report clearly outlines performance against KPIs.\n"
        elif context == "Decision Support":
            improved_prompt += "Tasks: Evaluate options, analyze pros and cons, and assess risks.\n\n"
            improved_prompt += "Output Expectations: Provide recommendations, business impact, and risk mitigation strategies.\n\n"
            improved_prompt += "Success Criteria: The decision is justified with clear trade-offs and recommendations.\n"
        elif context == "Workflow Design":
            improved_prompt += "Tasks: Outline process stages, define roles, and map dependencies.\n\n"
            improved_prompt += "Output Expectations: Provide a detailed process map, stage descriptions, and responsible roles.\n\n"
            improved_prompt += "Success Criteria: The workflow is documented end-to-end with no missing dependencies.\n"
        else:
            improved_prompt += "Tasks: Execute operational activities safely and efficiently.\n\n"
            improved_prompt += "Output Expectations: Provide specific actions, findings, and a structured summary.\n\n"
            improved_prompt += "Success Criteria: The operation completes with required quality standards.\n"

        # Note: A real LLM would be instructed by the system prompt to mitigate risks and incorporate diagnosis.
        # Here we assume the system prompt asked to include necessary structural elements, which our template fulfills.

        return improved_prompt
