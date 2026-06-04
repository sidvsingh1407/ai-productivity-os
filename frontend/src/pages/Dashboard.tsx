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

    // Check if the audit has contradictions or missing data which we treat as "Unresolved Findings" for this demo.
    const unresolvedCount = (lastAudit.contradictions?.length || 0) + (lastAudit.missing_data_flags?.length || 0);
    const findingsText = unresolvedCount > 0 ? `${unresolvedCount} Structural Anomalies Detected` : 'Baseline Stabilized';

    return `Last Assessment: ${daysText} — ${findingsText}`;
  };

  // Helper for determining the weakest dimension in the last audit
  const getWeakestDimension = (scores: any) => {
    if (!scores) return null;
    let weakest = null;
    let minScore = 101;
    for (const [dim, score] of Object.entries(scores)) {
      if (typeof score === 'number' && score < minScore) {
        minScore = score;
        weakest = dim;
      }
    }
    return weakest;
  };

  const weakestDimension = getWeakestDimension(lastAudit?.scores);

  // Helper for verdict
  const getVerdictText = (score: number, govScore: number) => {
    if (score > 75) return "Strong capability with minor operational optimizations required.";
    if (score >= 50) {
      if (govScore < 50) return "Moderate adoption undermined by significant governance vulnerabilities.";
      return "Developing capability with structural bottlenecks preventing scale.";
    }
    return "Critical structural vulnerabilities preventing successful integration.";
  };

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
          <h2 className="text-h2 text-text-primary mb-4">No structural assessments completed.</h2>
          <p className="text-body text-text-secondary max-w-2xl mx-auto mb-8">
            Run your first AI Audit to establish an operational baseline and identify areas requiring attention.
          </p>
          <button
            onClick={() => navigate('/audits/new')}
            className="px-8 py-4 bg-text-primary text-text-inverse text-body font-medium transition-colors hover:bg-text-primary/90"
          >
            Run AI Audit
          </button>
        </div>
      ) : (
        <div className="space-y-8">
          {/* --- Primary Card: Most Recent Assessment Summary --- */}
          {lastAudit && (
            <div className="border border-border-strong bg-bg-primary">
              <div className="p-8 border-b border-border-strong">
                <h3 className="text-label text-text-secondary mb-2">Most Recent Assessment</h3>
                <h2 className="text-h2 text-text-primary mb-4">{lastAudit.company_name || 'Organization'} AI Readiness</h2>
                <div className="text-body text-text-secondary max-w-3xl">
                  {getVerdictText(lastAudit.total_score, lastAudit.scores?.governance || 0)}
                  {' '}
                  <span className="font-mono text-data ml-2">Score: {lastAudit.total_score}/100</span>
                </div>
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

          {/* --- Secondary Card: Recommended Next Action --- */}
          {lastAudit && (
            <div className="border border-border-strong bg-bg-primary p-8">
              <h3 className="text-label text-text-secondary mb-2">Recommended Action</h3>
              <p className="text-h3 font-medium text-text-primary mb-6">
                {weakestDimension
                  ? `${weakestDimension.charAt(0).toUpperCase() + weakestDimension.slice(1)} capability is the primary operational bottleneck.`
                  : 'Diagnostic complete.'} Run Workflow Diagnostic to evaluate targeted execution.
              </p>
              <button
                onClick={() => navigate(`/workflows/new${lastAudit ? `?auditId=${lastAudit.id}` : ''}`)}
                className="px-6 py-3 border border-border-strong bg-bg-primary text-text-primary text-body font-medium transition-colors hover:bg-bg-secondary"
              >
                Run Workflow Diagnostic
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
