import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation } from '@tanstack/react-query';
import apiClient from '@/api/client';
import { ShieldAlert } from 'lucide-react';

import {
  ReportHeader,
  ExecutiveSummaryCard,
  AssessmentOverviewCard,
  ScoreBreakdown,
  CurrentTargetStateTable,
  FindingCard,
  RecommendationCard,
  RoadmapTimeline
} from '@/components/report';

export default function AuditDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [downloadJobId, setDownloadJobId] = useState<string | null>(null);

  const { data: audit, isLoading, isError } = useQuery({
    queryKey: ['audit', id],
    queryFn: async () => {
      const response = await apiClient.get(`/audits/${id}`);
      return response.data;
    },
    enabled: !!id,
  });

  const generatePdfMutation = useMutation({
    mutationFn: async () => {
      const response = await apiClient.post(`/reports/export/${id}`);
      return response.data;
    },
    onSuccess: (data) => {
      setDownloadJobId(data.job_id);
    },
  });

  const { data: jobStatus } = useQuery({
    queryKey: ['reportStatus', downloadJobId],
    queryFn: async () => {
      const response = await apiClient.get(`/reports/status/${downloadJobId}`);
      return response.data;
    },
    enabled: !!downloadJobId,
    refetchInterval: (query) => (query.state.data?.status === 'completed' ? false : 3000),
  });

  if (isLoading) return <div className="max-w-4xl mx-auto py-16 text-center text-text-secondary">Loading intelligence report...</div>;
  if (isError) return <div className="max-w-4xl mx-auto py-16 text-center text-accent-red">Error loading intelligence report.</div>;
  if (!audit) return <div className="max-w-4xl mx-auto py-16 text-center text-text-secondary">Report not found.</div>;

  const {
    scores = {},
    company_name = "Organization",
    total_score = 0,
    evidence_quality_score = 0,
    confidence_index = 0,
    rating = "Needs Improvement",
    compliance_risk_flag,
    compliance_risk_reasons,
    intelligence,
    created_at
  } = audit;

  const date = created_at ? new Date(created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }) : 'Unknown Date';

  // Map backend scores to the Dimension Breakdown
  const dimensions = [
    { label: 'Awareness', score: (scores.awareness || 0) * 5, keyFinding: (scores.awareness || 0) * 5 < 50 ? 'Knowledge silos prevent broad understanding.' : 'General awareness is established across target groups.' },
    { label: 'Adoption', score: (scores.adoption || 0) * 5, keyFinding: (scores.adoption || 0) * 5 < 50 ? 'Adoption is localized and largely informal.' : 'Active usage observed across key workflows.' },
    { label: 'Integration', score: (scores.integration || 0) * 5, keyFinding: (scores.integration || 0) * 5 < 50 ? 'Systems lack the infrastructure for deep integration.' : 'Core software is structurally prepared for automation.' },
    { label: 'Governance', score: (scores.governance || 0) * 5, keyFinding: (scores.governance || 0) * 5 < 50 ? 'Severe lack of oversight and formal policy.' : 'Oversight committees and guidelines are active.' },
    { label: 'ROI', score: (scores.roi || 0) * 5, keyFinding: (scores.roi || 0) * 5 < 50 ? 'No formal measurement of capability impact.' : 'Metrics are tracked against operational baselines.' },
  ];

  return (
    <div className="max-w-5xl mx-auto py-12 px-6">

      {jobStatus?.status === 'completed' && jobStatus?.download_url && (
        <div className="mb-8 p-4 bg-bg-secondary border border-border-strong flex justify-between items-center">
          <p className="text-body text-text-primary">
            PDF Export generated successfully.
          </p>
          <a href={jobStatus.download_url} className="text-body font-medium underline text-text-primary" target="_blank" rel="noreferrer">
            Download Report
          </a>
        </div>
      )}

      {compliance_risk_flag && (
        <div className="mb-8 p-6 bg-accent-red/5 border border-accent-red/20 flex gap-4 items-start">
          <ShieldAlert className="w-6 h-6 text-accent-red shrink-0" />
          <div>
            <h4 className="text-h3 font-medium text-accent-red mb-2">Compliance Risk Identified</h4>
            <p className="text-body text-accent-red/80">
              {compliance_risk_reasons?.[0] || "Governance issues detected requiring immediate review."}
            </p>
          </div>
        </div>
      )}

      <ReportHeader
        organizationName={company_name}
        reportTitle="AI Readiness Diagnostic"
        date={date}
        version="1.0"
      />

      {intelligence?.executive_summary ? (
        <ExecutiveSummaryCard
          overallAssessment={intelligence.executive_summary.overall_assessment}
          criticalRisk={intelligence.executive_summary.critical_risk}
          biggestOpportunity={intelligence.executive_summary.primary_opportunity}
          recommendedFirstAction={intelligence.executive_summary.recommended_first_action}
          onExportPdf={() => generatePdfMutation.mutate()}
        />
      ) : (
        <div className="mb-12 p-6 border border-border-strong bg-bg-secondary text-text-secondary">
          Executive summary intelligence unavailable.
        </div>
      )}

      <AssessmentOverviewCard
        overallScore={total_score}
        rating={rating}
        confidenceIndex={confidence_index}
        evidenceQuality={evidence_quality_score}
      />

      <ScoreBreakdown dimensions={dimensions} />

      {intelligence?.target_state && intelligence.target_state.length > 0 && (
        <CurrentTargetStateTable targetState={intelligence.target_state} />
      )}

      {intelligence?.findings && intelligence.findings.length > 0 && (
        <div className="mb-12">
          <h2 className="text-h2 font-semibold text-text-primary mb-6 border-b border-border-light pb-4">Prioritized Findings</h2>
          <div>
            {intelligence.findings.map((finding: any, idx: number) => (
              <FindingCard
                key={idx}
                number={idx + 1}
                title={finding.title}
                severity={finding.severity}
                impact={finding.impact}
                rationale={finding.rationale}
              />
            ))}
          </div>
        </div>
      )}

      {intelligence?.recommendations && intelligence.recommendations.length > 0 && (
        <div className="mb-12">
          <h2 className="text-h2 font-semibold text-text-primary mb-6 border-b border-border-light pb-4">Prioritized Recommendations</h2>
          <div>
            {intelligence.recommendations.map((rec: any, idx: number) => (
              <RecommendationCard
                key={idx}
                number={idx + 1}
                recommendation={rec.recommendation}
                priority={rec.priority}
                expectedImpact={rec.expected_impact}
                implementationEffort={rec.implementation_effort}
              />
            ))}
          </div>
        </div>
      )}

      {intelligence?.roadmap && (
        <RoadmapTimeline roadmap={intelligence.roadmap} />
      )}

      <div className="mb-8 p-6 bg-bg-secondary border border-border-strong mt-12">
        <h4 className="text-h4 font-medium text-text-primary mb-2">Assessment Limitations</h4>
        <p className="text-body text-text-secondary">
          This assessment is based on self-reported organizational responses and should be used as a directional decision-support tool rather than a substitute for a full organizational review.
        </p>
      </div>

      <div className="mt-8 pt-8 border-t border-border-strong text-center">
        <button
          onClick={() => navigate(`/workflows/new?auditId=${id}`)}
          className="px-8 py-4 bg-text-primary text-text-inverse text-body font-medium transition-colors hover:bg-text-primary/90"
        >
          Run Workflow Diagnostic
        </button>
      </div>

      <div className="mt-24 pt-8 border-t border-border-light text-center">
        <p className="text-data text-text-secondary">
          Generated by TarkaX Operational Intelligence Platform
        </p>
      </div>

    </div>
  );
}
