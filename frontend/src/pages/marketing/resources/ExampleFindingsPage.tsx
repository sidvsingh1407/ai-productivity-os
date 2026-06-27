import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '@/api/client';
import { SeoHead } from '../../../components/geo/SeoHead';
import { ReportHeader, ExecutiveSummaryCard, ScoreBreakdown } from '@/components/report';
import { ShieldAlert, Loader2 } from 'lucide-react';

export default function ExampleFindingsPage() {
  const navigate = useNavigate();
  const [auditData, setAuditData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchSample = async () => {
      try {
        const response = await apiClient.get('/sample-report');
        setAuditData(response.data);
      } catch (err) {
        console.error(err);
        setError(true);
      } finally {
        setLoading(false);
      }
    };
    fetchSample();
  }, []);

  if (loading) {
    return (
      <div className="bg-bg-primary min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-text-secondary" />
      </div>
    );
  }

  if (error || !auditData) {
    return (
      <div className="bg-bg-primary min-h-screen flex flex-col items-center justify-center p-6 text-center">
        <h2 className="text-h2 font-semibold text-text-primary mb-4">Report Generation Failed</h2>
        <p className="text-body text-text-secondary mb-6">Unable to generate the example findings via the deterministic engine.</p>
        <button onClick={() => navigate('/')} className="text-accent-blue font-medium hover:underline">Return Home</button>
      </div>
    );
  }

  const {
    scores,
    compliance_risk_flag,
    compliance_risk_reasons,
    contradictions
  } = auditData;

  const date = new Date(auditData.created_at).toLocaleDateString();

  return (
    <div className="bg-bg-primary min-h-screen">
      <SeoHead
        title="Example Findings | TarkaX"
        description="View an example of the hidden insights TarkaX reveals about business operations."
        canonical="https://tarkax.com/example-findings"
      />

      <div className="bg-bg-secondary border-b border-border-light py-8 px-6 text-center mb-8">
        <h1 className="text-h2 font-bold text-text-primary mb-2">Example Findings</h1>
        <p className="text-body text-text-secondary">This is a simulated example of the hidden insights TarkaX reveals about your business operations.</p>
      </div>

      <div className="max-w-5xl mx-auto py-4 px-6 pb-24">

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
          organizationName="Acme Corp (Example)"
          reportTitle="AI Readiness Diagnostic"
          date={date}
          version="1.0"
        />

        <div className="mb-8 p-6 bg-bg-secondary border border-border-strong">
          <h4 className="text-h4 font-medium text-text-primary mb-2">Assessment Limitations</h4>
          <p className="text-body text-text-secondary">
            This assessment is based on self-reported organizational responses. Results indicate potential strengths, risks, and opportunities but should not be considered a substitute for a full organizational review.
          </p>
        </div>

        {auditData?.intelligence?.executive_summary ? (
          <ExecutiveSummaryCard
            overallAssessment={auditData.intelligence.executive_summary.overall_assessment}
            criticalRisk={auditData.intelligence.executive_summary.critical_risk}
            biggestOpportunity={auditData.intelligence.executive_summary.primary_opportunity}
            recommendedFirstAction={auditData.intelligence.executive_summary.recommended_first_action}
          />
        ) : (
          <div className="mb-12 p-6 border border-border-strong bg-bg-secondary text-text-secondary">
            Executive summary intelligence unavailable.
          </div>
        )}

        <ScoreBreakdown dimensions={[
          { label: 'Awareness', score: (scores.awareness || 0) * 5, keyFinding: (scores.awareness || 0) * 5 < 50 ? 'Knowledge silos prevent broad understanding.' : 'General awareness is established across target groups.' },
          { label: 'Adoption', score: (scores.adoption || 0) * 5, keyFinding: (scores.adoption || 0) * 5 < 50 ? 'Adoption is localized and largely informal.' : 'Active usage observed across key workflows.' },
          { label: 'Integration', score: (scores.integration || 0) * 5, keyFinding: (scores.integration || 0) * 5 < 50 ? 'Systems lack the infrastructure for deep integration.' : 'Core software is structurally prepared for automation.' },
          { label: 'Governance', score: (scores.governance || 0) * 5, keyFinding: (scores.governance || 0) * 5 < 50 ? 'Severe lack of oversight and formal policy.' : 'Oversight committees and guidelines are active.' },
          { label: 'ROI', score: (scores.roi || 0) * 5, keyFinding: (scores.roi || 0) * 5 < 50 ? 'No formal measurement of capability impact.' : 'Metrics are tracked against operational baselines.' },
        ]} />

        {contradictions && contradictions.length > 0 && (
          <div className="mb-12 mt-12">
            <h2 className="text-h2 font-semibold text-text-primary mb-6 border-b border-border-light pb-4">Critical Contradictions</h2>
            <div className="space-y-4">
              {contradictions.map((contradiction: string, idx: number) => (
                <div key={idx} className="p-6 border border-border-strong bg-bg-secondary">
                  <p className="text-body text-text-primary">{contradiction}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="mt-16 text-center border-t border-border-light pt-12">
          <h3 className="text-h3 font-semibold text-text-primary mb-4">Want insights like these for your organization?</h3>
          <div className="flex justify-center gap-4">
             <button onClick={() => navigate('/contact')} className="px-6 py-3 bg-text-primary text-bg-primary font-medium rounded-md hover:opacity-90">
               Request a Demo
             </button>
             <button onClick={() => navigate('/ai-audit')} className="px-6 py-3 border border-border-strong text-text-primary font-medium rounded-md hover:bg-bg-secondary">
               Learn About Compliance Readinesss
             </button>
          </div>
        </div>

      </div>
    </div>
  );
}
