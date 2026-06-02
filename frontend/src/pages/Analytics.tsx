import React from 'react';
import { useQuery } from '@tanstack/react-query';
import apiClient  from '@/api/client';
import { ScoreTrendLine } from '@/components/charts/ScoreTrendLine';
import { Activity, BarChart2, ShieldCheck, Target } from 'lucide-react';

export default function Analytics() {
  const { data: volumeData, isLoading: isLoadingVolume } = useQuery({
    queryKey: ['analytics', 'volume'],
    queryFn: async () => {
      const { data } = await apiClient.get('/analytics/volume');
      return data; // { total_audits: 42, audits_this_month: 12 }
    },
  });

  const { data: complianceData, isLoading: isLoadingCompliance } = useQuery({
    queryKey: ['analytics', 'compliance'],
    queryFn: async () => {
      const { data } = await apiClient.get('/analytics/compliance');
      return data; // { compliance_rate: 85.5 }
    },
  });

  const { data: scoresData, isLoading: isLoadingScores } = useQuery({
    queryKey: ['analytics', 'scores'],
    queryFn: async () => {
      const { data } = await apiClient.get('/analytics/scores?days=30');
      return data; // { avg_score: 76.4, trend: [{date: '2023-10-01', score: 75}, ...] }
    },
  });

  const { data: dimensionsData, isLoading: isLoadingDimensions } = useQuery({
    queryKey: ['analytics', 'dimensions'],
    queryFn: async () => {
      const { data } = await apiClient.get('/analytics/dimensions');
      return data; // { awareness: 80, adoption: 65, integration: 70, governance: 85, roi: 60 }
    },
  });

  const isLoading = isLoadingVolume || isLoadingCompliance || isLoadingScores || isLoadingDimensions;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Analytics Dashboard</h1>
        <p className="text-sm text-slate-500">Overview of your organization's performance and compliance.</p>
      </div>

      {isLoading ? (
        <div className="flex h-64 items-center justify-center">
          <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-t-2 border-slate-900"></div>
        </div>
      ) : (
        <>
          {/* Stat Cards */}
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <StatCard
              title="Total Audits"
              value={volumeData?.total_audits || 0}
              icon={<BarChart2 className="h-5 w-5 text-slate-500" />}
            />
            <StatCard
              title="Avg Score"
              value={scoresData?.avg_score ? `${scoresData.avg_score.toFixed(1)}/100` : 'N/A'}
              icon={<Target className="h-5 w-5 text-slate-500" />}
            />
            <StatCard
              title="Compliance Rate"
              value={complianceData?.compliance_rate ? `${complianceData.compliance_rate.toFixed(1)}%` : 'N/A'}
              icon={<ShieldCheck className="h-5 w-5 text-slate-500" />}
            />
            <StatCard
              title="Audits This Month"
              value={volumeData?.audits_this_month || 0}
              icon={<Activity className="h-5 w-5 text-slate-500" />}
            />
          </div>

          <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
            {/* Trend Chart */}
            <div className="lg:col-span-2">
              <ScoreTrendLine data={scoresData?.trend || []} />
            </div>

            {/* Dimension Averages */}
            <div className="rounded-lg border border-slate-200 bg-white p-4">
              <h3 className="mb-4 text-sm font-medium text-slate-800">Dimension Averages</h3>
              <div className="space-y-4">
                {dimensionsData && Object.entries(dimensionsData).map(([key, val]) => (
                  <DimensionBar key={key} name={key} value={Number(val)} />
                ))}
                {!dimensionsData && (
                  <p className="text-sm text-slate-500">No dimension data available.</p>
                )}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

function StatCard({ title, value, icon }: { title: string; value: string | number; icon: React.ReactNode }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-slate-500">{title}</h3>
        {icon}
      </div>
      <p className="mt-2 text-3xl font-bold text-slate-900">{value}</p>
    </div>
  );
}

function DimensionBar({ name, value }: { name: string; value: number }) {
  const formattedName = name.charAt(0).toUpperCase() + name.slice(1);
  return (
    <div>
      <div className="mb-1 flex justify-between text-sm">
        <span className="font-medium text-slate-700">{formattedName}</span>
        <span className="text-slate-500">{value.toFixed(1)}</span>
      </div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-slate-100">
        <div
          className="h-full bg-slate-800 transition-all duration-500"
          style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
        />
      </div>
    </div>
  );
}
