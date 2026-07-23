import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { aiSystemsApi } from '@/api/aiSystems';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Edit, Database } from 'lucide-react';

export default function AiSystemsList() {
  const navigate = useNavigate();

  const { data: systems, isLoading, isError } = useQuery({
    queryKey: ['ai-systems'],
    queryFn: aiSystemsApi.list,
  });

  if (isLoading) return <div className="p-8 text-center text-slate-500">Loading AI systems...</div>;
  if (isError) return <div className="p-8 text-center text-red-500">Error loading AI systems.</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">AI System Inventory</h1>
          <p className="text-slate-500 mt-2">Manage your organization's registered AI systems.</p>
        </div>
        <Button onClick={() => navigate('/app/ai-systems/new')}>
          New AI System
        </Button>
      </div>

      <div className="rounded-md border" style={{ background: 'var(--tx-bg-card)' }}>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Purpose</TableHead>
              <TableHead>Decision Making Role</TableHead>
              <TableHead>Criticality</TableHead>
              <TableHead>Lifecycle Status</TableHead>
              <TableHead>Department</TableHead>
              <TableHead>Data Owner</TableHead>
              <TableHead>Data Freshness</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {!systems || systems.length === 0 ? (
              <TableRow>
                <TableCell colSpan={10} className="text-center text-slate-500 py-8">
                  No AI systems found.
                </TableCell>
              </TableRow>
            ) : (
              systems.map((system) => {
                let statusVariant: 'default' | 'secondary' | 'outline' | 'destructive' = 'default';
                if (system.status === 'inactive') statusVariant = 'secondary';
                if (system.status === 'archived') statusVariant = 'outline';

                return (
                  <TableRow key={system.id}>
                    <TableCell className="font-medium">
                      <div className="flex items-center gap-2">
                        <Database className="w-4 h-4 text-slate-400" />
                        {system.name}
                      </div>
                    </TableCell>
                    <TableCell className="max-w-xs truncate" title={system.purpose}>
                      {system.purpose || 'N/A'}
                    </TableCell>
                    <TableCell className="max-w-xs truncate" title={system.decision_making_role}>
                      {system.decision_making_role}
                    </TableCell>
                    <TableCell className="max-w-[120px] truncate" title={system.criticality}>
                      {system.criticality || 'N/A'}
                    </TableCell>
                    <TableCell className="max-w-[120px] truncate" title={system.lifecycle_status}>
                      {system.lifecycle_status || 'N/A'}
                    </TableCell>
                    <TableCell className="max-w-[120px] truncate" title={system.department}>
                      {system.department || 'N/A'}
                    </TableCell>
                    <TableCell className="max-w-[120px] truncate" title={system.data_owner}>
                      {system.data_owner || 'N/A'}
                    </TableCell>
                    <TableCell className="max-w-[120px] truncate capitalize" title={system.data_freshness}>
                      {system.data_freshness ? system.data_freshness.replace('_', ' ') : 'N/A'}
                    </TableCell>
                    <TableCell>
                      <Badge variant={statusVariant} className="capitalize">
                        {system.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <Button variant="ghost" size="sm" onClick={() => navigate(`/app/ai-systems/${system.id}/edit`)}>
                        <Edit className="mr-2 h-4 w-4" /> Edit
                      </Button>
                    </TableCell>
                  </TableRow>
                );
              })
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
