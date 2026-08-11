import { useQuery } from '@tanstack/react-query';
import { organizationsApi } from '@/api/organizations';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { AlertCircle, LineChart, DollarSign, PieChart, Info } from 'lucide-react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

export default function FinancialIntelligencePage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['financial-intelligence'],
    queryFn: organizationsApi.getFinancialIntelligence,
  });

  if (isLoading) return <div className="p-8 text-center text-slate-500 font-sans">Loading Financial Intelligence...</div>;
  if (isError) return <div className="p-8 text-center text-red-500 font-sans">Error loading Financial Intelligence.</div>;
  if (!data) return null;

  const { org_cost, cost_by_criticality } = data;

  const formatCurrency = (val: number) => {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(val);
  };

  return (
    <div className="space-y-6 font-sans">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900" style={{ fontFamily: 'Barlow Condensed, sans-serif' }}>Financial Intelligence (6.5)</h1>
          <p className="text-slate-500 mt-2">Organization-level AI cost and financial breakdown.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card style={{ background: 'var(--tx-bg-card)' }}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <DollarSign className="w-5 h-5 text-blue-600" />
              Total Organization Cost Rollup
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="mb-4">
              <span className="text-4xl font-bold text-slate-900 font-mono">
                {formatCurrency(org_cost.total)}
              </span>
              <span className="text-sm text-slate-500 ml-2">Total Computed Cost</span>
            </div>

            {org_cost.is_partial && (
              <div className="bg-amber-50 border border-amber-200 text-amber-800 p-3 rounded-md flex items-start gap-2 mb-4">
                <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
                <div className="text-sm">
                  <strong>Partial Data Warning:</strong> One or more AI systems are missing explicit cost metrics, making this total incomplete.
                </div>
              </div>
            )}

            <div className="text-sm text-slate-600 border-t pt-4">
              Systems with fully or partially reported costs: <strong className="font-mono text-slate-900">{org_cost.systems_with_data}</strong> out of <strong className="font-mono text-slate-900">{org_cost.total_systems}</strong>
            </div>
          </CardContent>
        </Card>

        <Card style={{ background: 'var(--tx-bg-card)' }}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Info className="w-5 h-5 text-blue-600" />
              Methodology
            </CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-slate-600 space-y-4">
            <p>
              The Financial Intelligence engine aggregates hard costs (Licensing, Cloud Compute, Inference API usage, and Maintenance) across all tracked AI systems.
            </p>
            <p>
              <strong>Strict Aggregation:</strong> Null values are not silently coerced to $0.00. If any system is missing cost data components, the resulting total is flagged as partial to prevent underestimating liability.
            </p>
          </CardContent>
        </Card>
      </div>

      <Card style={{ background: 'var(--tx-bg-card)' }}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <PieChart className="w-5 h-5 text-blue-600" />
            Cost by System Criticality
          </CardTitle>
        </CardHeader>
        <CardContent>
          {Object.keys(cost_by_criticality).length === 0 ? (
            <p className="text-slate-500 text-sm">No criticality data available.</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Criticality Tier</TableHead>
                  <TableHead className="text-right">Systems Tracked</TableHead>
                  <TableHead className="text-right">Total Cost</TableHead>
                  <TableHead className="text-right">Data Quality</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {Object.entries(cost_by_criticality).map(([tier, costData]) => (
                  <TableRow key={tier}>
                    <TableCell className="font-medium capitalize">{tier}</TableCell>
                    <TableCell className="text-right font-mono">{costData.total_systems}</TableCell>
                    <TableCell className="text-right font-mono">{formatCurrency(costData.total)}</TableCell>
                    <TableCell className="text-right">
                      {costData.is_partial ? (
                        <span className="text-amber-600 text-xs font-semibold flex items-center justify-end gap-1">
                          <AlertCircle className="w-3 h-3" /> Partial
                        </span>
                      ) : (
                        <span className="text-emerald-600 text-xs font-semibold">
                           Complete
                        </span>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
