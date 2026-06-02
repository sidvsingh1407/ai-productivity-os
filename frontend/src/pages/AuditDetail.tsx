import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation } from '@tanstack/react-query';
import apiClient from '@/api/client';
import { ScoreRadarChart } from '@/components/charts/ScoreRadarChart';
import { DimensionBar } from '@/components/charts/DimensionBar';
import { ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { ComplianceAlert } from '@/components/audits/ComplianceAlert';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { FileDown, PlaySquare, RotateCcw } from 'lucide-react';

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

  const { data: previousAudit } = useQuery({
    queryKey: ['previousAudit', id],
    queryFn: async () => {
      // Fetch latest 2 to find the one preceding this one
      const response = await apiClient.get('/audits/?limit=10');
      const audits = response.data?.items || [];
      const currentIndex = audits.findIndex((a: any) => a.id === id);
      if (currentIndex >= 0 && currentIndex < audits.length - 1) {
        return audits[currentIndex + 1];
      }
      return null;
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

  if (isLoading) return <div>Loading audit details...</div>;
  if (isError) return <div>Error loading audit details.</div>;
  if (!audit) return <div>Audit not found.</div>;

  const {
    scores = {},
    company_name = "Company",
    rating = "N/A",
    compliance_risk_flag,
    compliance_risk_reasons,
    contradictions,
    missing_data_flags,
    evidence_quality_score,
    confidence_index
  } = audit;

  const totalScore = Object.values(scores as Record<string, number>).reduce((acc, val) => acc + val, 0);

  const getConfidenceLevel = (score: number | null | undefined) => {
    if (score === null || score === undefined) return null;
    if (score < 40) return { label: 'Low Confidence', color: 'text-red-700', bg: 'bg-red-50', border: 'border-red-200' };
    if (score < 70) return { label: 'Medium Confidence', color: 'text-amber-700', bg: 'bg-amber-50', border: 'border-amber-200' };
    return { label: 'High Confidence', color: 'text-green-700', bg: 'bg-green-50', border: 'border-green-200' };
  };

  const getEQSLevel = (score: number | null | undefined) => {
    if (score === null || score === undefined) return null;
    if (score <= 20) return 'L1';
    if (score <= 40) return 'L2';
    if (score <= 60) return 'L3';
    if (score <= 80) return 'L4';
    return 'L5';
  };

  const confidence = getConfidenceLevel(confidence_index);
  const eqsLevel = getEQSLevel(evidence_quality_score);

  const radarData = [
    { subject: 'Awareness', A: scores.awareness || 0, fullMark: 20 },
    { subject: 'Adoption', A: scores.adoption || 0, fullMark: 20 },
    { subject: 'Integration', A: scores.integration || 0, fullMark: 20 },
    { subject: 'Governance', A: scores.governance || 0, fullMark: 20 },
    { subject: 'ROI', A: scores.roi || 0, fullMark: 20 },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">{company_name} Audit</h1>
          <p className="text-slate-500">ID: {id}</p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline" onClick={() => navigate(`/audits/new?sourceAuditId=${id}`)}>
            <RotateCcw className="mr-2 h-4 w-4" />
            Re-Run Audit
          </Button>
          <Button variant="outline" onClick={() => generatePdfMutation.mutate()} disabled={generatePdfMutation.isPending || !!downloadJobId}>
            <FileDown className="mr-2 h-4 w-4" />
            {generatePdfMutation.isPending ? 'Generating...' : 'Download PDF'}
          </Button>
          <Button onClick={() => navigate(`/workflows/new?auditId=${id}`)}>
            <PlaySquare className="mr-2 h-4 w-4" />
            Run Workflow Diagnostic
          </Button>
        </div>
      </div>

      {jobStatus?.status === 'completed' && jobStatus?.download_url && (
        <div className="bg-green-50 p-4 rounded-md border border-green-200">
          <p className="text-green-800">
            PDF Report is ready! <a href={jobStatus.download_url} className="font-bold underline" target="_blank" rel="noreferrer">Click here to download</a>
          </p>
        </div>
      )}

      {compliance_risk_flag && (
        <ComplianceAlert reasons={compliance_risk_reasons || ['Governance issues detected.']} />
      )}

      {confidence && (
        <Card className={`${confidence.border} ${confidence.bg}`}>
          <CardContent className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="col-span-1 border-r border-slate-200/50">
                <p className={`text-sm font-semibold uppercase tracking-wider mb-1 ${confidence.color}`}>Confidence Index</p>
                <div className="flex items-baseline space-x-2">
                  <span className={`text-4xl font-bold ${confidence.color}`}>{confidence_index}%</span>
                </div>
                <p className={`text-sm mt-1 font-medium ${confidence.color}`}>{confidence.label}</p>
              </div>
              <div className="col-span-1 border-r border-slate-200/50 pl-4">
                <p className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-1">Evidence Quality</p>
                <div className="flex items-baseline space-x-2">
                  <span className="text-3xl font-bold text-slate-800">{eqsLevel}</span>
                  <span className="text-sm text-slate-500">Score: {evidence_quality_score}</span>
                </div>
              </div>
              <div className="col-span-1 pl-4">
                <p className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-1">Contradictions</p>
                <div className="flex items-baseline space-x-2">
                  <span className={`text-3xl font-bold ${contradictions?.length > 0 ? 'text-red-600' : 'text-slate-800'}`}>{contradictions?.length || 0}</span>
                  <span className="text-sm text-slate-500">Detected</span>
                </div>
              </div>
            </div>

            {contradictions?.length > 0 && (
              <div className="mt-4 pt-4 border-t border-slate-200/50">
                <h4 className={`font-medium mb-2 ${confidence.color}`}>Detected Contradictions:</h4>
                <ul className={`list-disc pl-5 space-y-1 text-sm ${confidence.color}`}>
                  {contradictions.map((item: string, i: number) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              </div>
            )}

            {missing_data_flags?.length > 0 && (
              <div className="mt-4 pt-4 border-t border-slate-200/50">
                <h4 className={`font-medium mb-2 ${confidence.color}`}>Missing Data In Dimensions:</h4>
                <ul className={`list-disc pl-5 space-y-1 text-sm ${confidence.color}`}>
                  {missing_data_flags.map((item: string, i: number) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {(!confidence && (contradictions?.length > 0 || missing_data_flags?.length > 0)) && (
        <Card className="border-amber-200 bg-amber-50">
          <CardHeader>
            <CardTitle className="text-amber-800 text-lg">Assessment Findings</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {contradictions?.length > 0 && (
              <div>
                <h4 className="font-medium text-amber-900 mb-2">Contradictions Detected:</h4>
                <ul className="list-disc pl-5 space-y-1 text-sm text-amber-800">
                  {contradictions.map((item: string, i: number) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              </div>
            )}
            {missing_data_flags?.length > 0 && (
              <div>
                <h4 className="font-medium text-amber-900 mb-2">Missing Data In Dimensions:</h4>
                <ul className="list-disc pl-5 space-y-1 text-sm text-amber-800">
                  {missing_data_flags.map((item: string, i: number) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Total Score</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col items-center justify-center py-6">
            <div className="text-6xl font-bold text-slate-900 mb-4">{totalScore}</div>

            {previousAudit && (
              <div className={`flex items-center space-x-1 mb-4 text-lg font-medium ${totalScore >= (previousAudit.total_score || 0) ? 'text-green-600' : 'text-red-600'}`}>
                {totalScore >= (previousAudit.total_score || 0) ? <ArrowUpRight className="h-5 w-5" /> : <ArrowDownRight className="h-5 w-5" />}
                <span>{Math.abs(totalScore - (previousAudit.total_score || 0))} pts</span>
                <span className="text-sm text-slate-500 ml-1 font-normal">(vs previous)</span>
              </div>
            )}

            <Badge variant={totalScore > 75 ? "default" : totalScore > 50 ? "secondary" : "destructive"} className="text-lg py-1 px-4">
              {rating}
            </Badge>
          </CardContent>
        </Card>

        <Card className="col-span-1 md:col-span-2">
          <CardHeader>
            <CardTitle>Score Breakdown</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ScoreRadarChart data={radarData} />
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Dimensions Details</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <DimensionBar label="Awareness" score={scores.awareness || 0} />
          <DimensionBar label="Adoption" score={scores.adoption || 0} />
          <DimensionBar label="Integration" score={scores.integration || 0} />
          <DimensionBar label="Governance" score={scores.governance || 0} />
          <DimensionBar label="ROI" score={scores.roi || 0} />
        </CardContent>
      </Card>
    </div>
  );
}
