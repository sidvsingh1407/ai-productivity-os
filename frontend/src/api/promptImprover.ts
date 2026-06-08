import { apiClient } from './client';

export interface OperationalContext {
  detected_context: string;
  purpose: string;
  operational_environment: string;
}

export interface DiagnosisResponse {
  strength: string;
  missing_elements: string[];
  execution_risks: string[];
}

export interface ScoresResponse {
  original_score: number;
  improved_score: number;
}

export interface ValidationResponse {
  passed: boolean;
  validation_errors: string[];
}

export interface RationaleResponse {
  context_reasoning: string;
  changes_made: string[];
  failure_modes_addressed: string[];
  expected_improvements: string;
}

export interface PromptIntelligenceResponse {
  operational_context: OperationalContext;
  diagnosis: DiagnosisResponse;
  improved_prompt: string;
  improvement_rationale: RationaleResponse;
  intelligence_scores: ScoresResponse;
  validation: ValidationResponse;
}

export interface ValidationFailureResponse {
  validation: ValidationResponse;
}

export const promptImproverApi = {
  analyzePrompt: async (prompt: string): Promise<PromptIntelligenceResponse> => {
    const { data } = await apiClient.post('/prompt-improver', { prompt });
    return data;
  },
};
