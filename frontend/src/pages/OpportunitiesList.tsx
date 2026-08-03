import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { opportunitiesApi } from '@/api/opportunities';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { RefreshCw, Search } from 'lucide-react';
import { toast } from 'sonner';

export default function OpportunitiesList() {
  const queryClient = useQueryClient();
  const [filterAiSystem, setFilterAiSystem] = useState<string>('');

  const { data: response, isLoading, isError } = useQuery({
    queryKey: ['opportunities', filterAiSystem],
    queryFn: () => opportunitiesApi.list(filterAiSystem || undefined),
  });

  const generateMutation = useMutation({
    mutationFn: opportunitiesApi.generate,
    onSuccess: () => {
      toast.success('Opportunities generated successfully');
      queryClient.invalidateQueries({ queryKey: ['opportunities'] });
    },
    onError: () => {
      toast.error('Failed to generate opportunities');
    }
  });

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-slate-100 text-slate-800';
    }
  };

  const getCategoryColor = (category: string) => {
    const map: Record<string, string> = {
      manual_work: 'bg-blue-100 text-blue-800',
      repetitive_decisions: 'bg-purple-100 text-purple-800',
      knowledge_bottleneck: 'bg-orange-100 text-orange-800',
      customer_pain: 'bg-pink-100 text-pink-800',
      department_pain: 'bg-indigo-100 text-indigo-800',
      automation_candidate: 'bg-teal-100 text-teal-800',
    };
    return map[category] || 'bg-slate-100 text-slate-800';
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">Opportunity Discovery</h1>
          <p className="text-slate-500 mt-2">Identify where automation and AI can help.</p>
        </div>
        <Button
          onClick={() => generateMutation.mutate()}
          disabled={generateMutation.isPending}
          className="flex items-center gap-2"
        >
          <RefreshCw className={`h-4 w-4 ${generateMutation.isPending ? 'animate-spin' : ''}`} />
          Generate Opportunities
        </Button>
      </div>

      <div className="flex gap-4 items-center">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-2 top-2.5 h-4 w-4 text-slate-500" />
          <input
            type="text"
            placeholder="Filter by AI System ID (or 'null' for org-level)..."
            value={filterAiSystem}
            onChange={(e) => setFilterAiSystem(e.target.value)}
            className="pl-8 pr-4 py-2 w-full border rounded-md text-sm"
          />
        </div>
      </div>

      {isLoading ? (
        <div className="p-8 text-center text-slate-500">Loading opportunities...</div>
      ) : isError ? (
        <div className="p-8 text-center text-red-500">Error loading opportunities.</div>
      ) : (
        <div className="border rounded-md">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Title</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Priority</TableHead>
                <TableHead>Source</TableHead>
                <TableHead>Scope</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {response?.items.map((opp) => (
                <TableRow key={opp.id}>
                  <TableCell>
                    <div className="font-medium text-slate-900">{opp.title}</div>
                    <div className="text-sm text-slate-500 line-clamp-1">{opp.description}</div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="secondary" className={getCategoryColor(opp.category)}>
                      {opp.category.replace('_', ' ')}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant="secondary" className={getPriorityColor(opp.confidence_or_priority)}>
                      {opp.confidence_or_priority}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-sm text-slate-500 capitalize">
                    {opp.source_module.replace('_', ' ')}
                  </TableCell>
                  <TableCell className="text-sm text-slate-500">
                    {opp.ai_system_id ? (
                      <span className="font-mono text-xs" title={opp.ai_system_id}>
                        {opp.ai_system_id.substring(0, 8)}...
                      </span>
                    ) : (
                      'Org-level'
                    )}
                  </TableCell>
                </TableRow>
              ))}
              {!response?.items.length && (
                <TableRow>
                  <TableCell colSpan={5} className="text-center p-8 text-slate-500">
                    No opportunities found. Click "Generate Opportunities" to discover some.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  );
}
