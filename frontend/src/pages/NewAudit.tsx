import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import apiClient from '@/api/client';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';

// Sections mapping to q1_1 through q5_3
const SECTIONS = [
  {
    id: 1,
    title: 'Awareness',
    description: 'How aware is your organization of AI capabilities and risks?',
    questions: [
      { id: 'q1_1', text: 'Executive understanding of AI impact on industry' },
      { id: 'q1_2', text: 'Employee awareness of AI tools and acceptable use' },
      { id: 'q1_3', text: 'Dedicated budget for AI initiatives and training' },
    ],
  },
  {
    id: 2,
    title: 'Adoption',
    description: 'To what extent are AI tools currently being used?',
    questions: [
      { id: 'q2_1', text: 'Current adoption rate across departments' },
      { id: 'q2_2', text: 'Number of approved AI tools deployed' },
      { id: 'q2_3', text: 'Frequency of AI usage in daily workflows' },
    ],
  },
  {
    id: 3,
    title: 'Integration',
    description: 'How deeply is AI integrated into your systems?',
    questions: [
      { id: 'q3_1', text: 'Integration of AI with existing core software' },
      { id: 'q3_2', text: 'Data readiness and accessibility for AI models' },
      { id: 'q3_3', text: 'Custom models or fine-tuning capabilities' },
    ],
  },
  {
    id: 4,
    title: 'Governance',
    description: 'What policies and oversight govern AI usage?',
    questions: [
      { id: 'q4_1', text: 'Formal AI usage policy and guidelines' },
      { id: 'q4_2', text: 'Oversight committee or review process for new tools' },
      { id: 'q4_3', text: 'Compliance tracking (e.g., EU AI Act readiness)' },
    ],
  },
  {
    id: 5,
    title: 'ROI',
    description: 'Are you measuring the impact of AI?',
    questions: [
      { id: 'q5_1', text: 'Tracking time saved by AI automation' },
      { id: 'q5_2', text: 'Measuring cost reduction from AI deployment' },
      { id: 'q5_3', text: 'Revenue generation directly linked to AI features' },
    ],
  },
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

  const [currentSectionIndex, setCurrentSectionIndex] = useState(0);
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

  const currentSection = SECTIONS[currentSectionIndex];
  const isLastSection = currentSectionIndex === SECTIONS.length - 1;

  // Check if all questions in the current section are answered
  const isSectionComplete = currentSection.questions.every((q) => responses[q.id]);

  const handleSelect = (questionId: string, value: string) => {
    setResponses((prev) => ({ ...prev, [questionId]: value }));
  };

  const handleEvidenceChange = (questionId: string, field: 'evidence_url' | 'evidence_context', value: string) => {
    setEvidence((prev) => ({
      ...prev,
      [questionId]: {
        ...prev[questionId],
        [field]: value,
      },
    }));
  };

  const handleNext = () => {
    if (isSectionComplete && !isLastSection) {
      setCurrentSectionIndex((prev) => prev + 1);
    }
  };

  const handlePrev = () => {
    if (currentSectionIndex > 0) {
      setCurrentSectionIndex((prev) => prev - 1);
    }
  };

  const handleSubmit = async () => {
    if (!isSectionComplete) return;

    setIsSubmitting(true);
    setError(null);
    try {
      // Filter out empty evidence objects
      const filteredEvidence: Record<string, { evidence_url: string; evidence_context: string }> = {};
      Object.keys(evidence).forEach(key => {
        const ev = evidence[key];
        if (ev && (ev.evidence_url || ev.evidence_context)) {
          filteredEvidence[key] = {
            evidence_url: ev.evidence_url || "",
            evidence_context: ev.evidence_context || ""
          };
        }
      });

      const payload = { form_response: responses, evidence_response: filteredEvidence };
      const response = await apiClient.post('/audits/', payload);
      navigate(`/audits/${response.data.id}`);
    } catch (err: any) {
      console.error('Failed to submit audit:', err);
      setError(err.response?.data?.detail || 'Failed to submit audit. Please try again.');
      setIsSubmitting(false);
    }
  };

  if (isLoadingSource) {
    return <div className="max-w-2xl mx-auto py-8 text-center text-slate-500">Loading previous audit data...</div>;
  }

  return (
    <div className="max-w-2xl mx-auto py-8">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-light tracking-tight mb-2">Optimization Audit Engine</h1>
        <p className="text-muted-foreground">
          Step {currentSectionIndex + 1} of {SECTIONS.length}: {currentSection.title}
        </p>
        <div className="w-full bg-slate-200 h-2 mt-4 rounded-full">
          <div
            className="bg-primary h-2 rounded-full transition-all duration-300"
            style={{ width: `${((currentSectionIndex + 1) / SECTIONS.length) * 100}%` }}
          />
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>{currentSection.title}</CardTitle>
          <CardDescription>{currentSection.description}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {error && (
            <div className="bg-red-50 text-red-700 p-3 rounded-md text-sm mb-4 border border-red-200">
              {error}
            </div>
          )}

          {currentSection.questions.map((q) => (
            <div key={q.id} className="space-y-3">
              <label className="text-sm font-medium text-slate-900 block">
                {q.text}
              </label>
              <div className="grid gap-2">
                {OPTIONS.map((opt) => (
                  <label
                    key={opt.value}
                    className={`flex items-center space-x-3 p-3 border rounded-md cursor-pointer transition-colors ${
                      responses[q.id] === opt.value
                        ? 'bg-primary/5 border-primary/50'
                        : 'hover:bg-slate-50 border-slate-200'
                    }`}
                  >
                    <input
                      type="radio"
                      name={q.id}
                      value={opt.value}
                      checked={responses[q.id] === opt.value}
                      onChange={() => handleSelect(q.id, opt.value)}
                      className="text-primary focus:ring-primary h-4 w-4"
                    />
                    <span className="text-sm">{opt.label}</span>
                  </label>
                ))}
              </div>
              <div className="mt-4 p-4 bg-slate-50 rounded-md border border-slate-100">
                <p className="text-sm font-medium mb-3 text-slate-700">Supporting Evidence (Optional)</p>
                <div className="space-y-3">
                  <div>
                    <label className="text-xs text-slate-500 block mb-1">Evidence URL(s) (comma separated)</label>
                    <Input
                      placeholder="https://..."
                      value={evidence[q.id]?.evidence_url || ''}
                      onChange={(e) => handleEvidenceChange(q.id, 'evidence_url', e.target.value)}
                      className="text-sm"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-slate-500 block mb-1">Evidence Context & Explanation</label>
                    <Textarea
                      placeholder="Briefly explain the evidence..."
                      value={evidence[q.id]?.evidence_context || ''}
                      onChange={(e) => handleEvidenceChange(q.id, 'evidence_context', e.target.value)}
                      className="text-sm min-h-[80px]"
                    />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </CardContent>
        <CardFooter className="flex justify-between border-t p-6">
          <Button
            variant="outline"
            onClick={handlePrev}
            disabled={currentSectionIndex === 0 || isSubmitting}
          >
            Previous
          </Button>

          {isLastSection ? (
            <Button
              onClick={handleSubmit}
              disabled={!isSectionComplete || isSubmitting}
            >
              {isSubmitting ? 'Processing...' : 'Submit Audit'}
            </Button>
          ) : (
            <Button
              onClick={handleNext}
              disabled={!isSectionComplete}
            >
              Next
            </Button>
          )}
        </CardFooter>
      </Card>
    </div>
  );
}
