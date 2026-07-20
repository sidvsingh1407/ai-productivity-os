import apiClient from './client';

export interface SystemFindingResponse {
  ai_system_id: string;
  ai_system_name: string;
  findings: any[];
  recommendations: any[];
  executive_summary?: string;
  dimension_scores: Record<string, any>;
}

export interface AuditResponse {
  id: string;
  org_id: string;
  user_id: string;
  form_response?: Record<string, any>;
  evidence_response?: Record<string, any>;
  scores?: Record<string, any>;
  total_score?: number;
  evidence_quality_score?: number;
  confidence_index?: number;
  rating?: string;
  compliance_risk_flag?: boolean;
  compliance_risk_reasons?: string[];
  contradictions?: string[];
  missing_data_flags?: string[];

  intelligence?: any; // Keeping this broad 'any' to avoid mass refactoring of Dashboard/AuditDetail for now
  narrative_source?: string;
  system_findings?: SystemFindingResponse[];

  status: string;
  industry_type?: string;
  created_at: string;

  // Dashboard accesses company_name from lastAudit, which might come from a join or other API return value.
  company_name?: string;
}

export interface AuditListResponse {
  items: AuditResponse[];
  total: number;
  skip: number;
  limit: number;
}

export const auditsApi = {
  createAudit: async (data: any): Promise<AuditResponse> => {
    const response = await apiClient.post('/audits', data);
    return response.data;
  },
  getAudit: async (id: string): Promise<AuditResponse> => {
    const response = await apiClient.get(`/audits/${id}`);
    return response.data;
  },
  listAudits: async (): Promise<AuditListResponse> => {
    const response = await apiClient.get('/audits');
    return response.data;
  },
};
