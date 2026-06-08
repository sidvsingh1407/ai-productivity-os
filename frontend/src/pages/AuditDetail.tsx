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
  BenchmarkPerformanceSection,
  CurrentTargetStateTable,
  FindingCard,
  RecommendationCard,
  RoadmapTimeline,
  RiskSeverityCard,
  RiskTimeline,
  CostOfInactionTable
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

      {intelligence?.risk_projection && (
        <RiskSeverityCard
          riskLevel={intelligence.risk_projection.risk_level}
          riskScore={intelligence.risk_projection.risk_score}
          confidence={intelligence.risk_projection.confidence}
          topRiskDriver={intelligence.risk_projection.risk_drivers?.[0] || 'Unknown Risk Driver'}
          projectedImpactSummary={
            intelligence.risk_projection.risk_timeline?.near_term?.[0] ||
            intelligence.risk_projection.risk_drivers?.[0] ||
            (intelligence.cost_of_inaction?.[0]?.business_impact) ||
            'Immediate operational friction increases.'
          }
        />
      )}

      {intelligence?.cost_of_inaction && intelligence.cost_of_inaction.length > 0 && (
        <CostOfInactionTable coiData={intelligence.cost_of_inaction} />
      )}

      {intelligence?.risk_projection?.risk_timeline && (
        <RiskTimeline timeline={intelligence.risk_projection.risk_timeline} />
      )}

      <AssessmentOverviewCard
        overallScore={total_score}
        rating={rating}
        confidenceIndex={confidence_index}
        evidenceQuality={evidence_quality_score}
      />

      <ScoreBreakdown dimensions={dimensions} />

      <BenchmarkPerformanceSection benchmark={intelligence?.benchmark} yourScores={scores} />

      {intelligence?.operational_health && (
        <div className="mb-12">
          <h2 className="text-h2 font-semibold text-text-primary mb-6 border-b border-border-light pb-4">Predictive Intelligence</h2>

          <div className="bg-white rounded border border-gray-200 p-6 mb-6">
             <div className="flex justify-between items-center mb-4">
                 <h3 className="text-lg font-medium text-gray-900">Operational Health Index</h3>
                 <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-bold">{intelligence.operational_health.index}/100</span>
             </div>
             <p className="text-gray-600">{intelligence.operational_health.explanation}</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
             {intelligence?.risk_projection && (
               <div className="bg-white rounded border border-gray-200 p-6">
                 <h3 className="text-lg font-medium text-gray-900 mb-4">Risk Trajectory: <span className="font-bold text-red-600">{intelligence.risk_projection.risk_level}</span></h3>
                 <p className="text-sm text-gray-600 mb-4">{intelligence.risk_projection.explanation}</p>
                 <h4 className="text-sm font-semibold text-gray-900 mb-2">Key Drivers</h4>
                 <ul className="list-disc pl-5 text-sm text-gray-600">
                    {intelligence.risk_projection.risk_drivers.map((driver: string, i: number) => (
                      <li key={i}>{driver}</li>
                    ))}
                 </ul>
               </div>
             )}

             {intelligence?.early_warnings && intelligence.early_warnings.length > 0 && (
               <div className="bg-white rounded border border-gray-200 p-6">
                 <h3 className="text-lg font-medium text-gray-900 mb-4">Early Warnings</h3>
                 <div className="space-y-4">
                   {intelligence.early_warnings.map((warning: any, i: number) => (
                     <div key={i} className="bg-red-50 p-3 rounded border border-red-100">
                        <p className="font-semibold text-red-800 text-sm">{warning.warning}</p>
                        <p className="text-red-600 text-xs mt-1">{warning.suggested_action}</p>
                     </div>
                   ))}
                 </div>
               </div>
             )}
          </div>
        </div>
      )}


      {intelligence?.target_state && intelligence.target_state.length > 0 && (
        <CurrentTargetStateTable targetState={intelligence.target_state} />
      )}

      {intelligence?.failure_intelligence && intelligence.failure_intelligence.length > 0 && (
        <div className="mb-12">
          <h2 className="text-h2 font-semibold text-text-primary mb-6 border-b border-border-light pb-4">Failure Intelligence Analysis</h2>
          <div className="space-y-8">
            {intelligence.failure_intelligence.map((fi: any, idx: number) => (
              <div key={idx} className="p-6 bg-white border border-border-light rounded-md">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-h3 font-semibold text-text-primary">{fi.pattern}</h3>
                  <span className={`px-3 py-1 text-data font-medium rounded-full ${
                    fi.severity === 'Critical' ? 'bg-red-50 text-red-700 border border-red-200' :
                    fi.severity === 'Major' ? 'bg-orange-50 text-orange-700 border border-orange-200' :
                    'bg-yellow-50 text-yellow-700 border border-yellow-200'
                  }`}>
                    {fi.severity} Risk
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-6">
                  <div>
                    <h4 className="text-h4 font-medium text-text-secondary mb-2">Why Detected</h4>
                    <p className="text-body text-text-primary bg-bg-secondary p-3 rounded border border-border-light">{fi.why_detected}</p>
                  </div>
                  <div>
                    <h4 className="text-h4 font-medium text-text-secondary mb-2">Confidence Level</h4>
                    <div className="flex items-center">
                      <div className="w-full bg-border-light h-2 rounded-full mr-3">
                        <div className="bg-navy h-2 rounded-full" style={{ width: `${fi.confidence}%` }}></div>
                      </div>
                      <span className="text-data font-medium">{fi.confidence}%</span>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-6">
                  <div>
                    <h4 className="text-h4 font-medium text-text-secondary mb-2">Root Causes</h4>
                    <ul className="list-disc pl-5 text-body text-text-primary space-y-1">
                      {fi.root_causes.map((cause: string, i: number) => (
                        <li key={i}>{cause}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="text-h4 font-medium text-text-secondary mb-2">Operational Consequences</h4>
                    <ul className="list-disc pl-5 text-body text-text-primary space-y-1">
                      {fi.consequences.map((consequence: string, i: number) => (
                        <li key={i}>{consequence}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div>
                  <h4 className="text-h4 font-medium text-text-secondary mb-3">Recommended Actions</h4>
                  <div className="space-y-3">
                    {fi.recommended_actions.map((action: any, i: number) => (
                      <div key={i} className="bg-bg-secondary p-4 rounded border border-border-light flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                        <span className="text-body font-medium text-text-primary">{action.intervention}</span>
                        <div className="flex gap-3 shrink-0">
                          <span className="text-data bg-white px-2 py-1 border border-border-light rounded text-text-secondary">Impact: {action.impact}</span>
                          <span className="text-data bg-white px-2 py-1 border border-border-light rounded text-text-secondary">Effort: {action.effort}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

              </div>
            ))}
          </div>
        </div>
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
          onClick={() => navigate(`/app/workflows/new?auditId=${id}`)}
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
