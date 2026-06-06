import { apiClient } from './client';

export interface PromptIntelligenceResponse {
  context: {
    category: string;
    confidence: number;
  };
  diagnosis: {
    strength: string;
    missing: string[];
    execution_risks: string[];
  };
  scores: {
    original_score: number;
    improved_score: number;
  };
  validation: {
    passed: boolean;
    errors: string[];
  };
  improved_prompt: string;
  rationale: {
    changes_made: string[];
    failure_modes_addressed: string[];
  };
}

export const promptImproverApi = {
  analyzePrompt: async (prompt: string): Promise<PromptIntelligenceResponse> => {
    const { data } = await apiClient.post('/prompt-improver', { prompt });
    return data;
  },
};
