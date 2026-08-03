import React, { useCallback, useEffect, useState } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  Node,
  Edge,
  MarkerType,
  Panel,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import dagre from 'dagre';
import { DependencyNode, DependencyEdge, dependencyMapApi } from '@/api/dependencyMap';
import CustomNode, { CustomNodeData } from './CustomNode';
import { useQuery } from '@tanstack/react-query';
import { Button } from '../ui/button';
import { Loader2, RefreshCw } from 'lucide-react';

const nodeTypes = {
  custom: CustomNode,
};

interface DependencyGraphProps {
  nodes: DependencyNode[];
  edges: DependencyEdge[];
  getNodeLabel: (nodeId: string) => string;
  onNodeClick?: (nodeId: string) => void;
}

const getLayoutedElements = (nodes: Node[], edges: Edge[], direction = 'TB') => {
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));

  // Increase spacing for better readability
  const nodeWidth = 220;
  const nodeHeight = 120;

  dagreGraph.setGraph({ rankdir: direction, ranksep: 100, nodesep: 80 });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  const newNodes = nodes.map((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    return {
      ...node,
      position: {
        x: nodeWithPosition.x - nodeWidth / 2,
        y: nodeWithPosition.y - nodeHeight / 2,
      },
    };
  });

  return { nodes: newNodes, edges };
};

export default function DependencyGraph({ nodes: initialNodes, edges: initialEdges, getNodeLabel, onNodeClick }: DependencyGraphProps) {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [activeImpactId, setActiveImpactId] = useState<string | null>(null);

  // Fetch impact analysis if a node is selected
  const { data: impactData, isLoading: isImpactLoading } = useQuery({
    queryKey: ['impact-analysis', activeImpactId],
    queryFn: () => activeImpactId ? dependencyMapApi.getImpactAnalysis(activeImpactId) : Promise.resolve(null),
    enabled: !!activeImpactId,
  });

  const handleAnalyzeImpact = useCallback((nodeId: string) => {
    setActiveImpactId(nodeId);
  }, []);

  const resetImpact = useCallback(() => {
    setActiveImpactId(null);
  }, []);

  // Build the graph elements whenever dependencies or impact data changes
  useEffect(() => {
    if (!initialNodes || !initialEdges) return;
    if (initialNodes.length === 0) return;

    // Default states
    let flowNodes: Node<CustomNodeData>[] = initialNodes.map((n) => ({
      id: n.id,
      type: 'custom',
      position: { x: 0, y: 0 },
      data: {
        nodeId: n.id,
        label: getNodeLabel(n.id),
        type: n.node_type,
        highlightState: 'none',
        onAnalyzeImpact: handleAnalyzeImpact,
      },
    }));

    let flowEdges: Edge[] = initialEdges.map((e) => ({
      id: e.id,
      source: e.source_node_id,
      target: e.target_node_id,
      label: e.edge_type.replace('_', ' '),
      animated: false,
      style: { stroke: '#94a3b8', strokeWidth: 1.5 },
      markerEnd: {
        type: MarkerType.ArrowClosed,
        color: '#94a3b8',
      },
      labelStyle: { fill: '#475569', fontWeight: 500, fontSize: 12 },
      labelBgPadding: [4, 4],
      labelBgBorderRadius: 4,
      labelBgStyle: { fill: 'white', fillOpacity: 0.8 },
    }));

    // Apply Impact Analysis styles if active
    if (activeImpactId && impactData) {
      const upstreamSet = new Set(impactData.depends_on.map((n) => n.id));
      const downstreamSet = new Set(impactData.used_by.map((n) => n.id));

      flowNodes = flowNodes.map((n) => {
        let highlightState: CustomNodeData['highlightState'] = 'dimmed';
        let impactScore = undefined;
        let isOrigin = n.id === activeImpactId;

        if (isOrigin) {
          highlightState = 'none';
          impactScore = impactData.origin_impact;
        } else if (upstreamSet.has(n.id)) {
          highlightState = 'upstream';
          impactScore = impactData.depends_on.find((un) => un.id === n.id)?.impact;
        } else if (downstreamSet.has(n.id)) {
          highlightState = 'downstream';
          impactScore = impactData.used_by.find((dn) => dn.id === n.id)?.impact;
        }

        return {
          ...n,
          data: {
            ...n.data,
            highlightState,
            isOrigin,
            impact: impactScore,
          },
        };
      });

      flowEdges = flowEdges.map((e) => {
        const sourceInUp = upstreamSet.has(e.source) || e.source === activeImpactId;
        const targetInUp = upstreamSet.has(e.target) || e.target === activeImpactId;
        const isUpPath = sourceInUp && targetInUp && e.source !== e.target;

        const sourceInDown = downstreamSet.has(e.source) || e.source === activeImpactId;
        const targetInDown = downstreamSet.has(e.target) || e.target === activeImpactId;
        const isDownPath = sourceInDown && targetInDown && e.source !== e.target;

        if (isUpPath && !isDownPath) {
          return {
            ...e,
            animated: true,
            style: { stroke: '#f59e0b', strokeWidth: 2 }, // Amber
            markerEnd: { type: MarkerType.ArrowClosed, color: '#f59e0b' },
          };
        } else if (isDownPath && !isUpPath) {
          return {
            ...e,
            animated: true,
            style: { stroke: '#ef4444', strokeWidth: 2 }, // Red
            markerEnd: { type: MarkerType.ArrowClosed, color: '#ef4444' },
          };
        } else if (isUpPath && isDownPath) {
             return {
                ...e,
                animated: true,
                style: { stroke: '#8b5cf6', strokeWidth: 2 }, // Purple
                markerEnd: { type: MarkerType.ArrowClosed, color: '#8b5cf6' },
             }
        }

        return {
          ...e,
          style: { stroke: '#e2e8f0', strokeWidth: 1 }, // Dimmed
          markerEnd: { type: MarkerType.ArrowClosed, color: '#e2e8f0' },
          labelStyle: { fill: '#cbd5e1' }
        };
      });
    }

    // Apply layout
    const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(flowNodes, flowEdges);

    setNodes(layoutedNodes);
    setEdges(layoutedEdges);
  }, [initialNodes, initialEdges, getNodeLabel, activeImpactId, impactData, handleAnalyzeImpact, setNodes, setEdges]);

  return (
    <div className="w-full h-[600px] border rounded-md bg-slate-50/50 relative">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={(_, node) => onNodeClick && onNodeClick(node.id)}
        nodeTypes={nodeTypes}
        fitView
        minZoom={0.1}
        className="bg-slate-50/30"
      >
        <Background color="#cbd5e1" gap={20} size={1} />
        <Controls />
        <MiniMap
          nodeColor={(n) => {
            if (n.data.type === 'ai_system') return '#0B1F3A';
            if (n.data.type === 'workflow') return '#2563EB';
            return '#D97706';
          }}
          maskColor="rgba(248, 250, 252, 0.7)"
        />

        {activeImpactId && (
          <Panel position="top-right" className="bg-white p-4 rounded-md shadow-md border flex flex-col gap-2 min-w-[200px]">
            <h3 className="font-semibold text-sm">Impact Analysis Active</h3>

            {isImpactLoading ? (
              <div className="flex items-center text-sm text-slate-500 gap-2">
                <Loader2 className="w-4 h-4 animate-spin" />
                Analyzing...
              </div>
            ) : (
              <div className="flex flex-col gap-1 text-xs">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-amber-500" />
                  <span>Upstream (Depends On)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-red-500" />
                  <span>Downstream (Used By)</span>
                </div>
              </div>
            )}

            <Button size="sm" variant="outline" onClick={resetImpact} className="mt-2 w-full flex items-center gap-2">
              <RefreshCw className="w-3 h-3" />
              Reset View
            </Button>
          </Panel>
        )}
      </ReactFlow>
    </div>
  );
}