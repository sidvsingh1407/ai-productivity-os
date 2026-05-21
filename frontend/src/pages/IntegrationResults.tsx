import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import apiClient from '@/api/client';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ArrowLeft, AlertTriangle, CheckCircle2 } from 'lucide-react';

export default function IntegrationResults() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data, isLoading, isError } = useQuery({
    queryKey: ['integration', id],
    queryFn: async () => {
      const response = await apiClient.get(`/integration/${id}`);
      return response.data;
    },
    enabled: !!id,
  });

  if (isLoading) return <div>Loading integration results...</div>;
  if (isError) return <div>Error loading integration results.</div>;
  if (!data) return <div>Integration not found.</div>;

  const recommendations = data.recommendations || [];

  // Group by priority
  const highPriority = recommendations.filter((r: any) => r.priority === 'HIGH');
  const medPriority = recommendations.filter((r: any) => r.priority === 'MEDIUM');
  const lowPriority = recommendations.filter((r: any) => r.priority === 'LOW');

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <Button variant="ghost" size="icon" onClick={() => navigate(-1)}>
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">Integration Results</h1>
          <p className="text-slate-500">Analysis ID: {id}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Audit Summary</CardTitle>
          </CardHeader>
          <CardContent>
            {data.audit_summary ? (
              <div className="space-y-4">
                <div className="flex justify-between items-center border-b pb-2">
                  <span className="text-sm text-slate-500">Total Score</span>
                  <span className="font-bold text-lg">{data.audit_summary.total_score || 0}</span>
                </div>
                <div className="flex justify-between items-center border-b pb-2">
                  <span className="text-sm text-slate-500">Rating</span>
                  <Badge variant="outline">{data.audit_summary.rating || 'N/A'}</Badge>
                </div>
                <div className="pt-2">
                  <span className="text-sm text-slate-500 block mb-2">Dimension Breakdowns</span>
                  {data.audit_summary.scores && Object.entries(data.audit_summary.scores).map(([key, val]) => (
                    <div key={key} className="flex justify-between text-sm mb-1">
                      <span className="capitalize">{key}</span>
                      <span className="font-medium">{String(val)}/20</span>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <p className="text-sm text-slate-500">No summary available.</p>
            )}
          </CardContent>
        </Card>

        <Card className="col-span-1 md:col-span-2">
          <CardHeader>
            <CardTitle>Recommendations & Action Items</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">

            {highPriority.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-red-700 flex items-center mb-3">
                  <AlertTriangle className="mr-2 h-5 w-5" /> High Priority
                </h3>
                <div className="space-y-3">
                  {highPriority.map((r: any, idx: number) => (
                    <RecommendationItem key={idx} item={r} />
                  ))}
                </div>
              </div>
            )}

            {medPriority.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-yellow-600 flex items-center mb-3 border-t pt-4">
                  <CheckCircle2 className="mr-2 h-5 w-5" /> Medium Priority
                </h3>
                <div className="space-y-3">
                  {medPriority.map((r: any, idx: number) => (
                    <RecommendationItem key={idx} item={r} />
                  ))}
                </div>
              </div>
            )}

            {lowPriority.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-blue-600 flex items-center mb-3 border-t pt-4">
                  <CheckCircle2 className="mr-2 h-5 w-5" /> Low Priority
                </h3>
                <div className="space-y-3">
                  {lowPriority.map((r: any, idx: number) => (
                    <RecommendationItem key={idx} item={r} />
                  ))}
                </div>
              </div>
            )}

            {recommendations.length === 0 && (
              <p className="text-slate-500 italic">No specific recommendations generated.</p>
            )}

          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function RecommendationItem({ item }: { item: any }) {
  return (
    <div className={`p-4 rounded-lg border ${item.compliance_flag ? 'bg-red-50 border-red-200' : 'bg-white border-slate-200'}`}>
      <div className="flex justify-between items-start mb-2">
        <h4 className="font-semibold text-slate-900">{item.title || item.process_id || 'Action Item'}</h4>
        {item.compliance_flag && (
          <Badge variant="destructive" className="flex items-center text-xs">
            <AlertTriangle className="mr-1 h-3 w-3" /> Compliance Risk
          </Badge>
        )}
      </div>
      <p className="text-sm text-slate-600">{item.description}</p>
      {item.compliance_flag && item.warning_text && (
        <p className="text-xs text-red-600 mt-2 font-medium bg-red-100 p-2 rounded">
          ⚠️ {item.warning_text}
        </p>
      )}
    </div>
  );
}
