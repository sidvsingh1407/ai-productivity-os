import { useQuery } from '@tanstack/react-query';
import apiClient from '@/api/client';
import { useNavigate } from 'react-router-dom';

export function Dashboard() {
  const navigate = useNavigate();

  const { data: latestAudits, isLoading } = useQuery({
    queryKey: ['latestAudits'],
    queryFn: async () => {
      const response = await apiClient.get('/audits/?limit=1');
      return response.data?.items || [];
    },
  });

  const lastAudit = latestAudits?.[0];
  const intelligence = lastAudit?.intelligence;
  const dashboardPayload = intelligence?.dashboard;

  let daysSinceLastAudit = -1;
  if (lastAudit?.created_at) {
    const lastDate = new Date(lastAudit.created_at);
    daysSinceLastAudit = Math.floor((Date.now() - lastDate.getTime()) / (1000 * 60 * 60 * 24));
  }

  // --- Top Status Line ---
  const getStatusLine = () => {
    if (isLoading) return "Loading operational status...";
    if (!lastAudit) return "Status: No operational baseline established.";

    const daysText = daysSinceLastAudit === 0 ? 'Today' : `${daysSinceLastAudit} Days Ago`;

    // Fallback if we don't have intelligence findings yet, otherwise check findings
    const findingsCount = intelligence?.findings?.length || 0;
    const findingsText = findingsCount > 0 ? `${findingsCount} Structural Anomalies Detected` : 'Baseline Stabilized';

    return `Last Assessment: ${daysText} — ${findingsText}`;
  };

  // Helper for Card 1: Critical Risk
  const getCriticalRisk = () => {
    if (intelligence?.findings && intelligence.findings.length > 0) {
      // Find highest severity finding. We assume 'Critical' is highest, then 'High', 'Medium', 'Low'
      const severityOrder: Record<string, number> = { 'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1 };

      const highestSeverityFinding = intelligence.findings.reduce((prev: any, current: any) => {
        const prevScore = severityOrder[prev.severity] || 0;
        const currentScore = severityOrder[current.severity] || 0;
        return (currentScore > prevScore) ? current : prev;
      }, intelligence.findings[0]);

      return {
        title: highestSeverityFinding.title,
        severity: highestSeverityFinding.severity,
        impact: highestSeverityFinding.impact,
        rationale: highestSeverityFinding.rationale,
      };
    }

    if (dashboardPayload?.critical_risk) {
      return {
        title: "Critical Risk Identified",
        rationale: dashboardPayload.critical_risk,
        severity: null,
        impact: null,
      };
    }
    return null;
  };

  const criticalRisk = getCriticalRisk();

  // Helper for Card 2: Highest Priority Action
  const getPriorityAction = () => {
    if (intelligence?.recommendations && intelligence.recommendations.length > 0) {
      const topRec = intelligence.recommendations[0];
      return {
        recommendation: topRec.recommendation,
        priority: topRec.priority,
        expected_impact: topRec.expected_impact,
      };
    }

    if (dashboardPayload?.priority_action) {
      return {
        recommendation: dashboardPayload.priority_action,
        priority: null,
        expected_impact: null,
      };
    }
    return null;
  };

  const priorityAction = getPriorityAction();

  // Helper for Card 3: Fastest Improvement Opportunity
  const getImprovementOpportunity = () => {
    if (intelligence?.target_state && intelligence.target_state.length > 0) {
      // Weakest dimension is the one with the lowest current_score
      const weakest = intelligence.target_state.reduce((prev: any, current: any) => {
        return (current.current_score < prev.current_score) ? current : prev;
      }, intelligence.target_state[0]);

      return {
        dimension: weakest.dimension,
        current_score: weakest.current_score,
        target_score: weakest.target_score,
        rationale: weakest.rationale,
      };
    }

    if (dashboardPayload?.improvement_opportunity) {
      return {
        dimension: "Improvement Opportunity",
        rationale: dashboardPayload.improvement_opportunity,
        current_score: null,
        target_score: null,
      };
    }
    return null;
  };

  const improvementOpportunity = getImprovementOpportunity();

  return (
    <div className="max-w-5xl mx-auto py-12 px-6">
      <div className="mb-12">
        <h1 className="text-display text-text-primary mb-4">Decision Support Interface</h1>
        <p className="text-data text-text-secondary border-b border-border-strong pb-4">
          {getStatusLine()}
        </p>
      </div>

      {!isLoading && !lastAudit ? (
        // --- Empty State ---
        <div className="border border-border-strong bg-bg-primary p-12 text-center">
          <h2 className="text-h2 text-text-primary mb-4">No Assessments Yet</h2>
          <p className="text-body text-text-secondary max-w-2xl mx-auto mb-8">
            Run your first AI Audit to receive intelligence, recommendations, and risk insights.
          </p>
          <button
            onClick={() => navigate('/audits/new')}
            className="px-8 py-4 bg-text-primary text-text-inverse text-body font-medium transition-colors hover:bg-text-primary/90"
          >
            Start AI Audit
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          {/* --- Card 1: Most Critical Risk --- */}
          {criticalRisk && (
            <div className="border border-border-strong bg-bg-primary p-8">
              <h3 className="text-label text-text-secondary mb-4 uppercase tracking-wider">Most Critical Risk</h3>
              <h2 className="text-h2 text-text-primary mb-2">{criticalRisk.title}</h2>
              {criticalRisk.severity && criticalRisk.impact && (
                <div className="flex gap-6 mb-4">
                  <div>
                    <span className="text-label text-text-secondary uppercase">Severity: </span>
                    <span className="text-body font-medium text-text-primary">{criticalRisk.severity}</span>
                  </div>
                  <div>
                    <span className="text-label text-text-secondary uppercase">Impact: </span>
                    <span className="text-body font-medium text-text-primary">{criticalRisk.impact}</span>
                  </div>
                </div>
              )}
              <p className="text-body text-text-secondary max-w-3xl">
                {criticalRisk.rationale}
              </p>
            </div>
          )}

          {/* --- Card 2: Highest Priority Action --- */}
          {priorityAction && (
            <div className="border border-border-strong bg-bg-primary p-8">
              <h3 className="text-label text-text-secondary mb-4 uppercase tracking-wider">Highest Priority Action</h3>
              <h2 className="text-h2 text-text-primary mb-2">{priorityAction.recommendation}</h2>
              {priorityAction.priority && priorityAction.expected_impact && (
                <div className="flex gap-6 mt-4">
                  <div>
                    <span className="text-label text-text-secondary uppercase">Impact: </span>
                    <span className="text-body font-medium text-text-primary">{priorityAction.expected_impact}</span>
                  </div>
                  <div>
                    <span className="text-label text-text-secondary uppercase">Priority: </span>
                    <span className="text-body font-medium text-text-primary">{priorityAction.priority}</span>
                  </div>
                </div>
              )}
              {/* Optional CTA to run workflow diagnostic? Keeping it simple per spec. */}
              <div className="mt-8">
                <button
                  onClick={() => navigate(`/workflows/new${lastAudit ? `?auditId=${lastAudit.id}` : ''}`)}
                  className="px-6 py-3 border border-border-strong bg-bg-primary text-text-primary text-body font-medium transition-colors hover:bg-bg-secondary"
                >
                  Run Workflow Diagnostic
                </button>
              </div>
            </div>
          )}

          {/* --- Card 3: Fastest Improvement Opportunity --- */}
          {improvementOpportunity && (
            <div className="border border-border-strong bg-bg-primary p-8">
              <h3 className="text-label text-text-secondary mb-4 uppercase tracking-wider">Fastest Improvement Opportunity</h3>
              <h2 className="text-h2 text-text-primary capitalize mb-2">{improvementOpportunity.dimension}</h2>
              {improvementOpportunity.current_score !== null && improvementOpportunity.target_score !== null && (
                 <div className="flex gap-6 mb-4">
                  <div>
                    <span className="text-label text-text-secondary uppercase">Current: </span>
                    <span className="text-body font-mono font-medium text-text-primary">{improvementOpportunity.current_score}</span>
                  </div>
                  <div>
                    <span className="text-label text-text-secondary uppercase">Target: </span>
                    <span className="text-body font-mono font-medium text-text-primary">{improvementOpportunity.target_score}</span>
                  </div>
                </div>
              )}
              {improvementOpportunity.rationale && (
                <p className="text-body text-text-secondary max-w-3xl">
                  {improvementOpportunity.rationale}
                </p>
              )}
            </div>
          )}

          {/* --- Card 4: Latest Assessment Summary --- */}
          {lastAudit && (
            <div className="border border-border-strong bg-bg-primary">
              <div className="p-8 border-b border-border-strong">
                <h3 className="text-label text-text-secondary mb-4 uppercase tracking-wider">Latest Assessment Summary</h3>
                <div className="flex items-baseline gap-4 mb-4">
                  <h2 className="text-h2 text-text-primary">{lastAudit.company_name || 'Organization'} Assessment</h2>
                  {lastAudit.rating && (
                    <span className="text-body font-medium text-text-secondary px-3 py-1 bg-bg-secondary border border-border-strong rounded-full">
                      {lastAudit.rating}
                    </span>
                  )}
                  {lastAudit.total_score !== null && lastAudit.total_score !== undefined && (
                     <span className="font-mono text-data text-text-primary">Score: {lastAudit.total_score}/100</span>
                  )}
                </div>

                <p className="text-body text-text-secondary max-w-3xl">
                  {dashboardPayload?.executive_summary || "Assessment completed. Please refer to the full report for detailed insights."}
                </p>
              </div>
              <div className="p-6 bg-bg-secondary flex justify-end">
                <button
                  onClick={() => navigate(`/audits/${lastAudit.id}`)}
                  className="px-6 py-3 bg-text-primary text-text-inverse text-body font-medium transition-colors hover:bg-text-primary/90"
                >
                  View Full Report
                </button>
              </div>
            </div>
          )}

        </div>
      )}
    </div>
  );
}
