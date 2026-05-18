import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface AuditFormData {
  // Section 1: Company Information
  companyName: string;
  industry: string;
  numEmployees: string;
  primaryContactName: string;
  primaryContactEmail: string;
  jobTitle: string;

  // Section 2: AI Awareness
  leadershipUnderstanding: string;
  documentedStrategy: string;
  decisionMakingProcess: string;

  // Section 3: AI Adoption
  percentActivelyUsing: string;
  numToolsActive: string;
  usageFrequency: string;

  // Section 4: AI Integration
  integrationLevel: string;
  coreBusinessIntegration: string;
  workflowDocumentation: string;

  // Section 5: AI Governance
  usagePolicies: string;
  dataPrivacyHandling: string;
  euAiActStatus: string;

  // Section 6: AI ROI
  roiMeasurement: string;
  estimatedTimeSavings: string;
  overallBusinessImpact: string;

  // Section 7: Spend & Tools
  monthlySpend: string;
  toolsList: string;
  spendBreakdown: string;

  // Section 8: Consent
  contactConsent: string;
  benchmarkConsent: boolean;
}

const initialData: AuditFormData = {
  companyName: '',
  industry: '',
  numEmployees: '',
  primaryContactName: '',
  primaryContactEmail: '',
  jobTitle: '',
  leadershipUnderstanding: '',
  documentedStrategy: '',
  decisionMakingProcess: '',
  percentActivelyUsing: '',
  numToolsActive: '',
  usageFrequency: '',
  integrationLevel: '',
  coreBusinessIntegration: '',
  workflowDocumentation: '',
  usagePolicies: '',
  dataPrivacyHandling: '',
  euAiActStatus: '',
  roiMeasurement: '',
  estimatedTimeSavings: '',
  overallBusinessImpact: '',
  monthlySpend: '',
  toolsList: '',
  spendBreakdown: '',
  contactConsent: '',
  benchmarkConsent: false,
};

interface AuditStore {
  formData: AuditFormData;
  updateFormData: (data: Partial<AuditFormData>) => void;
  resetForm: () => void;
}

export const useAuditStore = create<AuditStore>()(
  persist(
    (set) => ({
      formData: initialData,
      updateFormData: (data) =>
        set((state) => ({
          formData: { ...state.formData, ...data },
        })),
      resetForm: () => set({ formData: initialData }),
    }),
    {
      name: 'audit-storage',
    }
  )
);
