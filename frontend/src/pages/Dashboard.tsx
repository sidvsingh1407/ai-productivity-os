import { useQuery } from '@tanstack/react-query';
import { useAuthStore } from '@/store/authStore';
import { analyticsApi } from '@/api/analytics';
import apiClient from '@/api/client';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Activity, Play, ShieldAlert, RotateCcw } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export function Dashboard() {
  const { user } = useAuthStore();
  const navigate = useNavigate();

  const { data: latestAudits } = useQuery({
    queryKey: ['latestAudits'],
    queryFn: async () => {
      const response = await apiClient.get('/audits/?limit=2');
      return response.data?.items || [];
    },
  });

  const { data: stats, isLoading, isError } = useQuery({
    queryKey: ['dashboardStats'],
    queryFn: async () => {
      // Trying to fetch from our analytics api wrappers.
      // If backend endpoints don't exist yet, we catch the error and return fallback data.
      try {
        const volume = await analyticsApi.getAuditVolume();
        const trend = await analyticsApi.getScoreTrend();
        const compliance = await analyticsApi.getComplianceRate();

        return {
          totalAudits: volume?.total || 0,
          lastScore: trend?.latestScore || 0,
          complianceStatus: compliance?.rate ? `${compliance.rate}%` : 'Unknown',
        };
      } catch (err) {
        // Fallback for when backend is not ready
        console.warn('Backend not ready, using fallback stats.', err);
        return {
          totalAudits: 0,
          lastScore: 0,
          complianceStatus: 'Pending',
        };
      }
    },
  });

  const lastAudit = latestAudits?.[0];
  const previousAudit = latestAudits?.[1];

  let daysSinceLastAudit = -1;
  if (lastAudit?.created_at) {
    const lastDate = new Date(lastAudit.created_at);
    daysSinceLastAudit = Math.floor((Date.now() - lastDate.getTime()) / (1000 * 60 * 60 * 24));
  }

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Welcome, {user?.full_name || 'User'}</h2>
        <p className="text-muted-foreground mt-2">
          Run your first audit or check your workflow diagnostics.
        </p>
      </div>

      {daysSinceLastAudit >= 0 && (
        <Card className="bg-primary/5 border-primary/20">
          <CardContent className="flex flex-col sm:flex-row items-center justify-between p-6">
            <div>
              <h3 className="font-semibold text-primary mb-1">Audit Reminder</h3>
              <p className="text-sm text-slate-600">
                {daysSinceLastAudit === 0 ? "You ran an audit today. Check back later to measure your progress." : `Your last audit was ${daysSinceLastAudit} day${daysSinceLastAudit > 1 ? 's' : ''} ago. Run another to measure progress.`}
              </p>
            </div>
            {daysSinceLastAudit > 0 && (
              <Button onClick={() => navigate(`/audits/new?sourceAuditId=${lastAudit.id}`)} className="mt-4 sm:mt-0 gap-2">
                <RotateCcw className="w-4 h-4" />
                Re-Run Audit
              </Button>
            )}
          </CardContent>
        </Card>
      )}

      <div className="flex gap-4">
        <Button className="gap-2" size="lg" onClick={() => navigate('/audits/new')}>
          <Play className="w-4 h-4" />
          Run AI Audit
        </Button>
        <Button variant="outline" className="gap-2" size="lg">
          <Activity className="w-4 h-4" />
          Run Workflow Diagnostic
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Audits</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {isLoading ? '-' : (isError ? 'Error' : stats?.totalAudits)}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Lifetime audits run
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Last Score</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="flex items-baseline space-x-2">
              <div className="text-2xl font-bold">
                {lastAudit ? lastAudit.total_score : (isLoading ? '-' : (isError ? 'Error' : stats?.lastScore))}
              </div>
              {previousAudit && lastAudit && (
                <div className={`text-sm font-semibold ${lastAudit.total_score >= previousAudit.total_score ? 'text-green-600' : 'text-red-600'}`}>
                  {lastAudit.total_score >= previousAudit.total_score ? '+' : ''}
                  {lastAudit.total_score - previousAudit.total_score} pts
                </div>
              )}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              {previousAudit ? `vs previous score: ${previousAudit.total_score}` : 'Latest audit performance'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Compliance Status</CardTitle>
            <ShieldAlert className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {isLoading ? '-' : (isError ? 'Error' : stats?.complianceStatus)}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Overall compliance health
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
