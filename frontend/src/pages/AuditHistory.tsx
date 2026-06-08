import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import apiClient from '@/api/client';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Eye, AlertTriangle, RotateCcw } from 'lucide-react';

export default function AuditHistory() {
  const navigate = useNavigate();
  const [page, setPage] = useState(1);
  const limit = 10;

  const { data, isLoading, isError } = useQuery({
    queryKey: ['audits', page],
    queryFn: async () => {
      const response = await apiClient.get(`/audits/?page=${page}&limit=${limit}`);
      return response.data; // assuming { items: [...], total: X } or just array
    },
  });

  const audits = Array.isArray(data) ? data : data?.items || [];

  if (isLoading) return <div>Loading history...</div>;
  if (isError) return <div>Error loading history.</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">Audit History</h1>
        <Button onClick={() => navigate('/app/audits/new')}>New Audit</Button>
      </div>

      <div className="rounded-md border" style={{ background: 'var(--tx-bg-card)' }}>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Date</TableHead>
              <TableHead>Company</TableHead>
              <TableHead>Total Score</TableHead>
              <TableHead>Rating</TableHead>
              <TableHead>Compliance Risk</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {audits.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center text-slate-500 py-8">
                  No audits found.
                </TableCell>
              </TableRow>
            ) : (
              audits.map((audit: any) => {
                const date = new Date(audit.created_at || Date.now()).toLocaleDateString();
                const totalScore = audit.scores ? Object.values(audit.scores as Record<string, number>).reduce((a, b) => a + b, 0) : 0;

                return (
                  <TableRow key={audit.id}>
                    <TableCell>{date}</TableCell>
                    <TableCell className="font-medium">{audit.company_name || 'N/A'}</TableCell>
                    <TableCell>{totalScore}/100</TableCell>
                    <TableCell>
                      <Badge variant="outline">{audit.rating || 'N/A'}</Badge>
                    </TableCell>
                    <TableCell>
                      {audit.compliance_risk_flag ? (
                        <div className="flex items-center text-red-600">
                          <AlertTriangle className="mr-1 h-4 w-4" /> Yes
                        </div>
                      ) : (
                        <span className="text-green-600">No</span>
                      )}
                    </TableCell>
                    <TableCell className="text-right flex justify-end space-x-2">
                      <Button variant="ghost" size="sm" onClick={() => navigate(`/app/audits/${audit.id}`)}>
                        <Eye className="mr-2 h-4 w-4" /> View
                      </Button>
                      <Button variant="outline" size="sm" onClick={() => navigate(`/app/audits/new?sourceAuditId=${audit.id}`)}>
                        <RotateCcw className="mr-2 h-4 w-4" /> Re-Run
                      </Button>
                    </TableCell>
                  </TableRow>
                );
              })
            )}
          </TableBody>
        </Table>
      </div>

      <div className="flex justify-between items-center mt-4">
        <Button
          variant="outline"
          onClick={() => setPage(p => Math.max(1, p - 1))}
          disabled={page === 1}
        >
          Previous
        </Button>
        <span className="text-sm text-slate-500">Page {page}</span>
        <Button
          variant="outline"
          onClick={() => setPage(p => p + 1)}
          disabled={audits.length < limit}
        >
          Next
        </Button>
      </div>
    </div>
  );
}
