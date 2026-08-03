import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { dependencyMapApi, DependencyEdge, DependencyNode } from '@/api/dependencyMap';
import { aiSystemsApi } from '@/api/aiSystems';
import { workflowsApi } from '@/api/workflows';
import { auditsApi } from '@/api/audits';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Trash2, Network, List, LayoutTemplate } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import DependencyGraph from '@/components/dependency-map/DependencyGraph';
import { ReactFlowProvider } from '@xyflow/react';
import { useState } from 'react';
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";

export default function DependencyMapList() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: edges, isLoading: edgesLoading } = useQuery({
    queryKey: ['dependency-edges'],
    queryFn: dependencyMapApi.listEdges,
  });

  const { data: nodes, isLoading: nodesLoading } = useQuery({
    queryKey: ['dependency-nodes'],
    queryFn: dependencyMapApi.listNodes,
  });

  const { data: systems = [] } = useQuery({ queryKey: ['ai-systems'], queryFn: aiSystemsApi.list });
  const { data: workflows = [] } = useQuery({ queryKey: ['workflows'], queryFn: workflowsApi.listWorkflows });
  const { data: auditsData } = useQuery({ queryKey: ['audits'], queryFn: auditsApi.listAudits });
  const audits = auditsData?.items || [];

  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  const deleteEdgeMutation = useMutation({
    mutationFn: dependencyMapApi.deleteEdge,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dependency-edges'] });
    },
  });

  const isLoading = edgesLoading || nodesLoading;

  const getNodeDisplayLabel = (nodeId: string) => {
    if (!nodes) return nodeId;
    const node = nodes.find(n => n.id === nodeId);
    if (!node) return nodeId;

    if (node.node_type === 'ai_system' && node.ai_system_id) {
      const sys = systems.find((s: any) => s.id === node.ai_system_id);
      return sys ? `AI System: ${sys.name}` : `AI System: ${node.ai_system_id.substring(0,8)}...`;
    }
    if (node.node_type === 'workflow' && node.workflow_id) {
      return `Workflow: ${node.workflow_id.substring(0,8)}...`;
    }
    if (node.node_type === 'audit' && node.audit_id) {
      return `Audit: ${node.audit_id.substring(0,8)}...`;
    }
    return nodeId;
  };

  const getSelectedNodeDetails = () => {
    if (!selectedNodeId || !nodes) return null;
    const node = nodes.find(n => n.id === selectedNodeId);
    if (!node) return null;

    let title = 'Unknown Node';
    let type = node.node_type;
    let description = '';
    let detailLink = '';

    if (node.node_type === 'ai_system' && node.ai_system_id) {
      const sys = systems.find((s: any) => s.id === node.ai_system_id);
      title = sys ? sys.name : 'AI System';
      description = sys ? sys.description : '';
      detailLink = `/app/ai-systems/${node.ai_system_id}/edit`;
    } else if (node.node_type === 'workflow' && node.workflow_id) {
      const wf = workflows.find((w: any) => w.id === node.workflow_id);
      title = wf ? wf.name : 'Workflow';
      description = wf ? wf.description : '';
      detailLink = `/app/workflows/${node.workflow_id}`;
    } else if (node.node_type === 'audit' && node.audit_id) {
      const audit = audits.find((a: any) => a.id === node.audit_id);
      title = audit ? (audit.system_name || 'Audit') : 'Audit';
      detailLink = `/app/audits/${node.audit_id}`;
    }

    return { node, title, type, description, detailLink };
  };

  const selectedNodeDetails = getSelectedNodeDetails();

  if (isLoading) return <div className="p-8 text-center text-slate-500">Loading Dependency Map...</div>;

  return (
    <div className="space-y-6 h-full flex flex-col">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">Dependency Map</h1>
          <p className="text-slate-500 mt-2">Manage relationships between AI systems, workflows, and audits.</p>
        </div>
        <Button onClick={() => navigate('/app/dependency-map/new')}>
          Add Relationship
        </Button>
      </div>

      <Tabs defaultValue="map" className="w-full flex-grow flex flex-col min-h-[700px]">
        <TabsList className="mb-4">
          <TabsTrigger value="map" className="flex items-center gap-2">
            <Network className="w-4 h-4" />
            Visual Map
          </TabsTrigger>
          <TabsTrigger value="list" className="flex items-center gap-2">
            <List className="w-4 h-4" />
            List View
          </TabsTrigger>
        </TabsList>

        <TabsContent value="map" className="mt-0 flex-grow relative h-full">
          <div className="bg-white rounded-md border p-4 h-[600px] absolute inset-0">
            <ReactFlowProvider>
              <DependencyGraph
                nodes={nodes || []}
                edges={edges || []}
                getNodeLabel={getNodeDisplayLabel}
                onNodeClick={setSelectedNodeId}
              />
            </ReactFlowProvider>
          </div>
        </TabsContent>

        <TabsContent value="list" className="mt-0">
          <div className="rounded-md border bg-white">
            <Table>
              <TableHeader>
            <TableRow>
              <TableHead>Source Entity</TableHead>
              <TableHead>Relationship (Edge)</TableHead>
              <TableHead>Target Entity</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {!edges || edges.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} className="text-center text-slate-500 py-8">
                  No relationships found.
                </TableCell>
              </TableRow>
            ) : (
              edges.map((edge) => (
                <TableRow key={edge.id}>
                  <TableCell className="font-medium">
                    {getNodeDisplayLabel(edge.source_node_id)}
                  </TableCell>
                  <TableCell>
                    <Badge variant="secondary" className="capitalize">
                      {edge.edge_type.replace('_', ' ')}
                    </Badge>
                  </TableCell>
                  <TableCell className="font-medium">
                    {getNodeDisplayLabel(edge.target_node_id)}
                  </TableCell>
                  <TableCell className="text-right">
                    <Button
                      variant="ghost"
                      size="sm"
                      className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      onClick={() => {
                        if(confirm('Are you sure you want to delete this relationship?')) {
                          deleteEdgeMutation.mutate(edge.id);
                        }
                      }}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
              </TableBody>
            </Table>
          </div>
        </TabsContent>
      </Tabs>

      <Sheet open={!!selectedNodeId} onOpenChange={(open) => !open && setSelectedNodeId(null)}>
        <SheetContent>
          <SheetHeader>
            <SheetTitle>{selectedNodeDetails?.title}</SheetTitle>
            <SheetDescription className="uppercase tracking-wider text-xs font-semibold mt-1">
              {selectedNodeDetails?.type.replace('_', ' ')}
            </SheetDescription>
          </SheetHeader>
          <div className="mt-6 space-y-4">
            {selectedNodeDetails?.description && (
              <div>
                <h4 className="text-sm font-medium text-slate-900 mb-1">Description</h4>
                <p className="text-sm text-slate-500">{selectedNodeDetails.description}</p>
              </div>
            )}

            <div className="pt-4 border-t">
              <Button
                variant="outline"
                className="w-full"
                onClick={() => {
                  if (selectedNodeDetails?.detailLink) {
                    navigate(selectedNodeDetails.detailLink);
                  }
                }}
              >
                View Full Details
              </Button>
            </div>
          </div>
        </SheetContent>
      </Sheet>

    </div>
  );
}
