import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import apiClient from '@/api/client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Check } from 'lucide-react';

// Re-structured questions to match the assessment dimensions into 3 form stages
// Note: The payload must still output responses keyed by q1_1, q2_1 etc.
const WIZARD_STAGES = [
  {
    id: 1,
    title: 'Organization Profile',
    description: 'Establish the operational baseline and demographic context.',
    questions: [
      { id: 'org_industry', text: 'Primary Industry', type: 'text' },
      { id: 'org_size', text: 'Organization Size (Employees)', type: 'text' },
      { id: 'org_department', text: 'Target Department / Scope', type: 'text' }
    ]
  },
  {
    id: 2,
    title: 'AI Stack Assessment',
    description: 'Evaluate awareness, adoption rate, and integration depth.',
    questions: [
      // Awareness (q1)
      { id: 'q1_1', text: 'Executive understanding of AI impact on industry', type: 'radio' },
      { id: 'q1_2', text: 'Employee awareness of AI tools and acceptable use', type: 'radio' },
      { id: 'q1_3', text: 'Dedicated budget for AI initiatives and training', type: 'radio' },
      // Adoption (q2)
      { id: 'q2_1', text: 'Current adoption rate across departments', type: 'radio' },
      { id: 'q2_2', text: 'Number of approved AI tools deployed', type: 'radio' },
      { id: 'q2_3', text: 'Frequency of AI usage in daily workflows', type: 'radio' },
      // Integration (q3)
      { id: 'q3_1', text: 'Integration of AI with existing core software', type: 'radio' },
      { id: 'q3_2', text: 'Data readiness and accessibility for AI models', type: 'radio' },
      { id: 'q3_3', text: 'Custom models or fine-tuning capabilities', type: 'radio' },
    ]
  },
  {
    id: 3,
    title: 'Governance Review',
    description: 'Assess oversight, risk management, and ROI tracking.',
    questions: [
      // Governance (q4)
      { id: 'q4_1', text: 'Formal AI usage policy and guidelines', type: 'radio' },
      { id: 'q4_2', text: 'Oversight committee or review process for new tools', type: 'radio' },
      { id: 'q4_3', text: 'Compliance tracking (e.g., EU AI Act readiness)', type: 'radio' },
      // ROI (q5)
      { id: 'q5_1', text: 'Tracking time saved by AI automation', type: 'radio' },
      { id: 'q5_2', text: 'Measuring cost reduction from AI deployment', type: 'radio' },
      { id: 'q5_3', text: 'Revenue generation directly linked to AI features', type: 'radio' },
    ]
  },
  {
    id: 4,
    title: 'Generate Report',
    description: 'Review structural findings and generate the operational intelligence report.',
    questions: [] // This step is just confirmation
  }
];

const OPTIONS = [
  { value: 'a', label: 'A: Fully Optimized / Mature' },
  { value: 'b', label: 'B: Active Progress / Scaling' },
  { value: 'c', label: 'C: Initial Steps / Emerging' },
  { value: 'd', label: 'D: Planning Stage / Low' },
  { value: 'e', label: 'E: No Action / None' },
];

export default function NewAudit() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const sourceAuditId = searchParams.get('sourceAuditId');

  const [currentStageIndex, setCurrentStageIndex] = useState(0);
  const [responses, setResponses] = useState<Record<string, string>>({});
  const [evidence, setEvidence] = useState<Record<string, { evidence_url: string; evidence_context: string }>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isLoadingSource, setIsLoadingSource] = useState(!!sourceAuditId);

  useEffect(() => {
    async function fetchSourceAudit() {
      if (sourceAuditId) {
        try {
          const res = await apiClient.get(`/audits/${sourceAuditId}`);
          if (res.data && res.data.form_response) {
            setResponses(res.data.form_response);
            // Ignore evidence loading for MVP simplicity unless explicitly needed
          }
        } catch (err) {
          console.error('Failed to load source audit', err);
        } finally {
          setIsLoadingSource(false);
        }
      }
    }
    fetchSourceAudit();
  }, [sourceAuditId]);

  const currentStage = WIZARD_STAGES[currentStageIndex];
  const isLastStage = currentStageIndex === WIZARD_STAGES.length - 1;

  const isStageComplete = currentStage.questions.every((q) => responses[q.id] && responses[q.id].trim() !== '');

  const handleSelect = (questionId: string, value: string) => {
    setResponses((prev) => ({ ...prev, [questionId]: value }));
  };

  const handleEvidenceChange = (questionId: string, field: 'evidence_url' | 'evidence_context', value: string) => {
    setEvidence((prev) => ({
      ...prev,
      [questionId]: {
        ...prev[questionId],
        [field]: value
      }
    }));
  };

  const handleNext = () => {
    if (isStageComplete) {
      setCurrentStageIndex((prev) => prev + 1);
      window.scrollTo(0, 0);
    }
  };

  const handlePrev = () => {
    if (currentStageIndex > 0) {
      setCurrentStageIndex((prev) => prev - 1);
      window.scrollTo(0, 0);
    }
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    setError(null);

    // Filter out metadata questions (org_*) to keep payload compliant with backend form_response expectation
    const formResponse = Object.keys(responses).reduce((acc, key) => {
      if (key.startsWith('q')) {
        acc[key] = responses[key];
      }
      return acc;
    }, {} as Record<string, string>);

    try {
      const res = await apiClient.post('/audits/', {
        form_response: formResponse,
        evidence_response: evidence
      });
      navigate(`/app/audits/${res.data.id}`);
    } catch (err: any) {
      console.error('Failed to submit audit:', err);
      setError(err.response?.data?.detail || 'Failed to submit audit. Please verify input and try again.');
      setIsSubmitting(false);
    }
  };

  if (isLoadingSource) {
    return <div className="max-w-4xl mx-auto py-16 text-center text-text-secondary">Loading source data...</div>;
  }

  return (
    <div className="max-w-6xl mx-auto py-12 px-6">
      <div className="mb-12 border-b border-border-strong pb-8">
        <h1 className="text-display text-text-primary mb-2">Compliance Readiness Assessment</h1>
        <p className="text-h3 text-text-secondary font-normal">Establish a structural baseline for artificial intelligence integration.</p>
      </div>

      <div className="flex flex-col lg:flex-row gap-12 items-start">
        {/* Vertical Progress Rail */}
        <div className="w-full lg:w-1/4 sticky top-12">
          <div className="border border-border-strong bg-bg-primary p-6">
            <h3 className="text-label text-text-secondary mb-6">Diagnostic Progress</h3>
            <ul className="space-y-6">
              {WIZARD_STAGES.map((stage, idx) => {
                const isActive = idx === currentStageIndex;
                const isCompleted = idx < currentStageIndex;
                return (
                  <li key={stage.id} className="flex gap-4 items-start relative">
                    {idx !== WIZARD_STAGES.length - 1 && (
                      <div className={`absolute left-[11px] top-6 bottom-[-24px] w-[2px] ${isCompleted ? 'bg-text-primary' : 'bg-border-light'}`} />
                    )}
                    <div className={`relative z-10 w-6 h-6 rounded-none flex items-center justify-center border text-data ${
                      isCompleted ? 'bg-text-primary border-text-primary text-text-inverse' :
                      isActive ? 'bg-bg-primary border-text-primary text-text-primary font-medium' :
                      'bg-bg-primary border-border-strong text-text-secondary'
                    }`}>
                      {isCompleted ? <Check className="w-3 h-3" /> : idx + 1}
                    </div>
                    <div className="pt-0.5">
                      <p className={`text-body ${isActive || isCompleted ? 'font-medium text-text-primary' : 'text-text-secondary'}`}>
                        {stage.title}
                      </p>
                    </div>
                  </li>
                );
              })}
            </ul>
          </div>
        </div>

        {/* Wizard Content */}
        <div className="w-full lg:w-3/4">
          <div className="border border-border-strong bg-bg-primary p-8 md:p-12">
            <div className="mb-12 border-b border-border-light pb-6">
              <h2 className="text-h2 text-text-primary mb-2">{currentStage.title}</h2>
              <p className="text-body text-text-secondary">{currentStage.description}</p>
            </div>

            {error && (
              <div className="bg-accent-red/10 border border-accent-red/20 text-accent-red p-4 mb-8 text-body">
                {error}
              </div>
            )}

            {currentStage.questions.length > 0 ? (
              <div className="space-y-12">
                {currentStage.questions.map((q, qIndex) => (
                  <div key={q.id} className="space-y-4">
                    <div className="flex gap-4 items-start">
                      <div className="text-h3 font-mono text-text-secondary pt-1 w-8">
                        {String(qIndex + 1).padStart(2, '0')}
                      </div>
                      <div className="flex-1">
                        <label className="text-h3 font-medium text-text-primary block mb-6">
                          {q.text}
                        </label>

                        {q.type === 'text' ? (
                          <Input
                            className="max-w-md rounded-none border-border-strong focus-visible:ring-text-primary"
                            value={responses[q.id] || ''}
                            onChange={(e) => handleSelect(q.id, e.target.value)}
                            placeholder="Enter details..."
                          />
                        ) : (
                          <div className="space-y-3">
                            {OPTIONS.map((opt) => (
                              <label
                                key={opt.value}
                                className={`flex items-center space-x-4 p-4 border cursor-pointer transition-colors ${
                                  responses[q.id] === opt.value
                                    ? 'bg-bg-secondary border-text-primary'
                                    : 'hover:bg-bg-secondary border-border-light'
                                }`}
                              >
                                <input
                                  type="radio"
                                  name={q.id}
                                  value={opt.value}
                                  checked={responses[q.id] === opt.value}
                                  onChange={() => handleSelect(q.id, opt.value)}
                                  className="text-text-primary focus:ring-text-primary h-4 w-4"
                                />
                                <span className="text-body text-text-primary">{opt.label}</span>
                              </label>
                            ))}
                          </div>
                        )}

                        {q.type === 'radio' && (
                          <div className="mt-8 border border-border-light bg-bg-secondary p-6">
                            <p className="text-label text-text-secondary mb-4">Structural Evidence (Optional)</p>
                            <div className="space-y-4">
                              <div>
                                <label className="text-body font-medium text-text-primary block mb-2">Evidence URL</label>
                                <Input
                                  placeholder="https://..."
                                  value={evidence[q.id]?.evidence_url || ''}
                                  onChange={(e) => handleEvidenceChange(q.id, 'evidence_url', e.target.value)}
                                  className="rounded-none border-border-strong focus-visible:ring-text-primary"
                                />
                              </div>
                              <div>
                                <label className="text-body font-medium text-text-primary block mb-2">Contextual Explanation</label>
                                <Textarea
                                  placeholder="Provide context for the current state..."
                                  value={evidence[q.id]?.evidence_context || ''}
                                  onChange={(e) => handleEvidenceChange(q.id, 'evidence_context', e.target.value)}
                                  className="rounded-none border-border-strong focus-visible:ring-text-primary min-h-[100px]"
                                />
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="py-12 text-center">
                <div className="w-16 h-16 bg-bg-secondary border border-border-strong flex items-center justify-center mx-auto mb-6">
                  <Check className="w-8 h-8 text-text-primary" />
                </div>
                <h3 className="text-h2 text-text-primary mb-4">Diagnostic Complete</h3>
                <p className="text-body text-text-secondary max-w-lg mx-auto">
                  All structural assessments have been recorded. Proceed to generate the final intelligence report.
                </p>
              </div>
            )}

            <div className="mt-12 pt-8 border-t border-border-strong flex justify-between items-center">
              <Button
                variant="outline"
                onClick={handlePrev}
                disabled={currentStageIndex === 0 || isSubmitting}
                className="rounded-none border-border-strong text-text-primary hover:bg-bg-secondary"
              >
                Previous Stage
              </Button>

              {isLastStage ? (
                <Button
                  onClick={handleSubmit}
                  disabled={isSubmitting}
                  className="rounded-none bg-text-primary text-text-inverse hover:bg-text-primary/90 px-8"
                >
                  {isSubmitting ? 'Processing Analysis...' : 'Generate Report'}
                </Button>
              ) : (
                <Button
                  onClick={handleNext}
                  disabled={!isStageComplete}
                  className="rounded-none bg-text-primary text-text-inverse hover:bg-text-primary/90 px-8"
                >
                  Proceed to Next Stage
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
