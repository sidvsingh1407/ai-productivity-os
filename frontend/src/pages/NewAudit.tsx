import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { apiClient } from '@/api/client';
import { useAuditStore } from '@/store/auditStore';
import { AuditFormStep } from '@/components/audits/AuditFormStep';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select } from '@/components/ui/select';

const industryOptions = [
  { value: 'Marketing/Advertising', label: 'Marketing/Advertising' },
  { value: 'SaaS/Technology', label: 'SaaS/Technology' },
  { value: 'Professional Services', label: 'Professional Services' },
  { value: 'Healthcare', label: 'Healthcare' },
  { value: 'Finance/FinTech', label: 'Finance/FinTech' },
  { value: 'E-commerce/Retail', label: 'E-commerce/Retail' },
  { value: 'Manufacturing', label: 'Manufacturing' },
  { value: 'Education', label: 'Education' },
  { value: 'Other', label: 'Other' },
];

const employeeOptions = [
  { value: '10-49', label: '10-49' },
  { value: '50-99', label: '50-99' },
  { value: '100-249', label: '100-249' },
  { value: '250-499', label: '250-499' },
  { value: '500+', label: '500+' },
];

export default function NewAudit() {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const totalSteps = 8;
  const { formData, updateFormData, resetForm } = useAuditStore();

  const mutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await apiClient.post('/audits/', { form_response: data });
      return response.data;
    },
    onSuccess: (data) => {
      resetForm();
      navigate(`/audits/${data.id}`);
    },
  });

  const handleNext = () => setCurrentStep((prev) => Math.min(prev + 1, totalSteps));
  const handlePrev = () => setCurrentStep((prev) => Math.max(prev - 1, 1));
  const handleSubmit = () => {
    mutation.mutate(formData);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target as any;
    const checked = type === 'checkbox' ? (e.target as HTMLInputElement).checked : undefined;
    updateFormData({ [name]: type === 'checkbox' ? checked : value });
  };

  return (
    <div className="container mx-auto py-8">
      {currentStep === 1 && (
        <AuditFormStep
          title="Company Information"
          currentStep={1}
          totalSteps={totalSteps}
          onNext={handleNext}
        >
          <div className="space-y-4">
            <div>
              <Label>Company Name</Label>
              <Input name="companyName" value={formData.companyName} onChange={handleChange} required />
            </div>
            <div>
              <Label>Industry</Label>
              <Select name="industry" value={formData.industry} onChange={handleChange} options={industryOptions} />
            </div>
            <div>
              <Label>Number of Employees</Label>
              <Select name="numEmployees" value={formData.numEmployees} onChange={handleChange} options={employeeOptions} />
            </div>
            <div>
              <Label>Primary Contact Name</Label>
              <Input name="primaryContactName" value={formData.primaryContactName} onChange={handleChange} required />
            </div>
            <div>
              <Label>Primary Contact Email</Label>
              <Input type="email" name="primaryContactEmail" value={formData.primaryContactEmail} onChange={handleChange} required />
            </div>
            <div>
              <Label>Job Title of Contact</Label>
              <Input name="jobTitle" value={formData.jobTitle} onChange={handleChange} required />
            </div>
          </div>
        </AuditFormStep>
      )}

      {currentStep === 2 && (
        <AuditFormStep
          title="AI Awareness"
          currentStep={2}
          totalSteps={totalSteps}
          onNext={handleNext}
          onPrev={handlePrev}
        >
          <div className="space-y-4">
            <div>
              <Label>Leadership understanding of AI</Label>
              <Select name="leadershipUnderstanding" value={formData.leadershipUnderstanding} onChange={handleChange} options={[
                { value: 'a', label: 'Very high - can articulate specific use cases' },
                { value: 'b', label: 'High - general understanding' },
                { value: 'c', label: 'Moderate - aware but vague' },
                { value: 'd', label: 'Low - minimal understanding' },
                { value: 'e', label: 'None' },
              ]} />
            </div>
            <div>
              <Label>Documented AI strategy</Label>
              <Select name="documentedStrategy" value={formData.documentedStrategy} onChange={handleChange} options={[
                { value: 'a', label: 'Yes, formally documented' },
                { value: 'b', label: 'Yes, but informal' },
                { value: 'c', label: 'In progress' },
                { value: 'd', label: 'Planning to create' },
                { value: 'e', label: 'No' },
              ]} />
            </div>
            <div>
              <Label>AI decision making process</Label>
              <Select name="decisionMakingProcess" value={formData.decisionMakingProcess} onChange={handleChange} options={[
                { value: 'a', label: 'Dedicated AI committee' },
                { value: 'b', label: 'Executive-led' },
                { value: 'c', label: 'Ad-hoc by department' },
                { value: 'd', label: 'Individual employees' },
                { value: 'e', label: 'No coordination' },
              ]} />
            </div>
          </div>
        </AuditFormStep>
      )}

      {currentStep === 3 && (
        <AuditFormStep
          title="AI Adoption"
          currentStep={3}
          totalSteps={totalSteps}
          onNext={() => {
            if (formData.numToolsActive === 'e') {
              setCurrentStep(7); // Skip to Section 7
            } else {
              handleNext();
            }
          }}
          onPrev={handlePrev}
        >
          <div className="space-y-4">
            <div>
              <Label>Percentage of employees actively using AI</Label>
              <Select name="percentActivelyUsing" value={formData.percentActivelyUsing} onChange={handleChange} options={[
                { value: 'a', label: '75% or more' },
                { value: 'b', label: '50-74%' },
                { value: 'c', label: '25-49%' },
                { value: 'd', label: '10-24%' },
                { value: 'e', label: 'Less than 10%' },
              ]} />
            </div>
            <div>
              <Label>Number of AI tools in active use</Label>
              <Select name="numToolsActive" value={formData.numToolsActive} onChange={handleChange} options={[
                { value: 'a', label: '6+ tools' },
                { value: 'b', label: '4-5 tools' },
                { value: 'c', label: '2-3 tools' },
                { value: 'd', label: '1 tool' },
                { value: 'e', label: 'None' },
              ]} />
            </div>
            {formData.numToolsActive !== 'e' && (
              <div>
                <Label>Usage frequency</Label>
                <Select name="usageFrequency" value={formData.usageFrequency} onChange={handleChange} options={[
                  { value: 'a', label: 'Daily' },
                  { value: 'b', label: 'Several times per week' },
                  { value: 'c', label: 'Weekly' },
                  { value: 'd', label: 'Monthly' },
                  { value: 'e', label: 'Rarely or never' },
                ]} />
              </div>
            )}
          </div>
        </AuditFormStep>
      )}

      {currentStep === 4 && (
        <AuditFormStep
          title="AI Integration"
          currentStep={4}
          totalSteps={totalSteps}
          onNext={handleNext}
          onPrev={handlePrev}
        >
          <div className="space-y-4">
            <div>
              <Label>Integration in tech stack</Label>
              <Select name="integrationLevel" value={formData.integrationLevel} onChange={handleChange} options={[
                { value: 'a', label: 'Deeply integrated (API, custom workflows)' },
                { value: 'b', label: 'Moderate integration' },
                { value: 'c', label: 'Light integration (standalone tools)' },
                { value: 'd', label: 'Minimal integration' },
                { value: 'e', label: 'No integration' },
              ]} />
            </div>
            <div>
              <Label>Core business systems integration (CRM, ERP, etc.)</Label>
              <Select name="coreBusinessIntegration" value={formData.coreBusinessIntegration} onChange={handleChange} options={[
                { value: 'a', label: 'Yes - integrated into core platform' },
                { value: 'b', label: 'Yes - integrated into some systems' },
                { value: 'c', label: 'Planning integration' },
                { value: 'd', label: 'Considering it' },
                { value: 'e', label: 'No' },
              ]} />
            </div>
            <div>
              <Label>Workflow documentation</Label>
              <Select name="workflowDocumentation" value={formData.workflowDocumentation} onChange={handleChange} options={[
                { value: 'a', label: 'Fully documented with training' },
                { value: 'b', label: 'Documented, informal training' },
                { value: 'c', label: 'Partial documentation' },
                { value: 'd', label: 'Ad-hoc knowledge sharing' },
                { value: 'e', label: 'No documentation' },
              ]} />
            </div>
          </div>
        </AuditFormStep>
      )}

      {currentStep === 5 && (
        <AuditFormStep
          title="AI Governance"
          currentStep={5}
          totalSteps={totalSteps}
          onNext={handleNext}
          onPrev={handlePrev}
        >
          <div className="space-y-4">
            <div>
              <Label>AI usage policies</Label>
              <Select name="usagePolicies" value={formData.usagePolicies} onChange={handleChange} options={[
                { value: 'a', label: 'Comprehensive policy with enforcement' },
                { value: 'b', label: 'Basic guidelines provided' },
                { value: 'c', label: 'Draft policy in development' },
                { value: 'd', label: 'Informal guidelines' },
                { value: 'e', label: 'No AI usage policy' },
              ]} />
            </div>
            <div>
              <Label>Data privacy handling</Label>
              <Select name="dataPrivacyHandling" value={formData.dataPrivacyHandling} onChange={handleChange} options={[
                { value: 'a', label: 'Formal review + approved tools only' },
                { value: 'b', label: 'Guidelines provided to employees' },
                { value: 'c', label: 'Ad-hoc review on request' },
                { value: 'd', label: 'Left to employee discretion' },
                { value: 'e', label: 'No oversight' },
              ]} />
            </div>
            <div>
              <Label>EU AI Act compliance status</Label>
              <Select name="euAiActStatus" value={formData.euAiActStatus} onChange={handleChange} options={[
                { value: 'a', label: 'Fully assessed and compliant' },
                { value: 'b', label: 'Assessment in progress' },
                { value: 'c', label: 'Aware but not started' },
                { value: 'd', label: 'Heard of it, no action' },
                { value: 'e', label: 'Unaware of EU AI Act' },
              ]} />
              {formData.euAiActStatus === 'e' && (
                <div className="mt-2 text-sm text-amber-600 bg-amber-50 p-2 rounded">
                  Note: The EU AI Act is a new regulation effective August 2026. Non-compliance can result in significant penalties.
                </div>
              )}
            </div>
          </div>
        </AuditFormStep>
      )}

      {currentStep === 6 && (
        <AuditFormStep
          title="AI ROI"
          currentStep={6}
          totalSteps={totalSteps}
          onNext={handleNext}
          onPrev={handlePrev}
        >
          <div className="space-y-4">
            <div>
              <Label>ROI measurement</Label>
              <Select name="roiMeasurement" value={formData.roiMeasurement} onChange={handleChange} options={[
                { value: 'a', label: 'Yes, formal metrics with regular review' },
                { value: 'b', label: 'Yes, informal tracking' },
                { value: 'c', label: 'Basic measurement (time estimates)' },
                { value: 'd', label: 'No, but planning to' },
                { value: 'e', label: 'No measurement' },
              ]} />
            </div>
            <div>
              <Label>Estimated time savings</Label>
              <Select name="estimatedTimeSavings" value={formData.estimatedTimeSavings} onChange={handleChange} options={[
                { value: 'a', label: '25% or more' },
                { value: 'b', label: '15-24%' },
                { value: 'c', label: '5-14%' },
                { value: 'd', label: 'Less than 5%' },
                { value: 'e', label: 'No measurable savings' },
              ]} />
            </div>
            <div>
              <Label>Overall business impact</Label>
              <Select name="overallBusinessImpact" value={formData.overallBusinessImpact} onChange={handleChange} options={[
                { value: 'a', label: 'Transformational' },
                { value: 'b', label: 'Significant' },
                { value: 'c', label: 'Moderate' },
                { value: 'd', label: 'Minimal' },
                { value: 'e', label: 'Negative/None' },
              ]} />
            </div>
          </div>
        </AuditFormStep>
      )}

      {currentStep === 7 && (
        <AuditFormStep
          title="Spend & Tools"
          currentStep={7}
          totalSteps={totalSteps}
          onNext={handleNext}
          onPrev={() => formData.numToolsActive === 'e' ? setCurrentStep(3) : handlePrev()}
        >
          <div className="space-y-4">
            <div>
              <Label>Total monthly AI spend</Label>
              <Select name="monthlySpend" value={formData.monthlySpend} onChange={handleChange} options={[
                { value: '< $500', label: '< $500' },
                { value: '$500-$2K', label: '$500-$2K' },
                { value: '$2K-$10K', label: '$2K-$10K' },
                { value: '$10K+', label: '$10K+' },
              ]} />
            </div>
            <div>
              <Label>List all AI tools currently in use</Label>
              <Input
                name="toolsList"
                value={formData.toolsList}
                onChange={handleChange}
                placeholder="e.g., ChatGPT, GitHub Copilot, Jasper..."
              />
            </div>
            <div>
              <Label>Breakdown of spend by tool (Optional)</Label>
              <Input
                name="spendBreakdown"
                value={formData.spendBreakdown}
                onChange={handleChange}
                placeholder="e.g., ChatGPT Enterprise: $500, Copilot: $1000..."
              />
            </div>
          </div>
        </AuditFormStep>
      )}

      {currentStep === 8 && (
        <AuditFormStep
          title="Consent & Submit"
          currentStep={8}
          totalSteps={totalSteps}
          onSubmit={handleSubmit}
          onPrev={handlePrev}
        >
          <div className="space-y-4">
            <div>
              <Label>May we contact you to discuss results?</Label>
              <Select name="contactConsent" value={formData.contactConsent} onChange={handleChange} options={[
                { value: 'Yes, happy to discuss', label: 'Yes, happy to discuss' },
                { value: 'Prefer report only', label: 'Prefer to receive report only' },
                { value: 'Critical only', label: 'Contact only if there are critical findings' },
              ]} />
            </div>
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="benchmarkConsent"
                name="benchmarkConsent"
                checked={formData.benchmarkConsent}
                onChange={handleChange}
                className="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-900"
              />
              <Label htmlFor="benchmarkConsent" className="font-normal text-slate-600">
                I consent to having my company's anonymized audit data used for industry benchmarking.
              </Label>
            </div>
            {mutation.isPending && <p>Submitting audit...</p>}
            {mutation.isError && <p className="text-red-500">Error submitting audit. Please try again.</p>}
          </div>
        </AuditFormStep>
      )}
    </div>
  );
}
