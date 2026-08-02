import React from 'react';
import { Handle, Position } from '@xyflow/react';
import { Badge } from '@/components/ui/badge';
import { Cpu, FileText, ClipboardCheck } from 'lucide-react';
import { ImpactScore } from '@/api/dependencyMap';

export type CustomNodeData = {
  label: string;
  type: 'ai_system' | 'workflow' | 'audit';
  impact?: ImpactScore;
  isOrigin?: boolean;
  highlightState?: 'none' | 'upstream' | 'downstream' | 'dimmed';
  onAnalyzeImpact?: (nodeId: string) => void;
  nodeId: string;
};

const CustomNode = ({ data }: { data: CustomNodeData }) => {
  const { label, type, impact, highlightState, isOrigin } = data;

  let bgColor = 'bg-white';
  let borderColor = 'border-slate-200';
  let textColor = 'text-slate-900';
  let Icon = Cpu;
  let typeLabel = 'System';

  // Apply base styling based on node type
  if (type === 'ai_system') {
    bgColor = 'bg-[#0B1F3A]'; // var(--bg-dark)
    borderColor = 'border-[#0B1F3A]';
    textColor = 'text-white';
    Icon = Cpu;
    typeLabel = 'AI System';
  } else if (type === 'workflow') {
    bgColor = 'bg-[#F8FAFC]'; // var(--bg-secondary)
    borderColor = 'border-[#2563EB]'; // var(--accent-blue)
    textColor = 'text-[#0F172A]'; // var(--text-primary)
    Icon = FileText;
    typeLabel = 'Workflow';
  } else if (type === 'audit') {
    bgColor = 'bg-[#F8FAFC]';
    borderColor = 'border-[#D97706]'; // var(--accent-amber)
    textColor = 'text-[#0F172A]';
    Icon = ClipboardCheck;
    typeLabel = 'Audit';
  }

  // Apply highlight state overrides
  let opacity = 'opacity-100';
  let glowEffect = '';

  if (highlightState === 'dimmed') {
    opacity = 'opacity-30';
  } else if (highlightState === 'upstream') {
    borderColor = 'border-amber-500'; // Amber for upstream
    glowEffect = 'shadow-[0_0_10px_rgba(245,158,11,0.5)]'; // Amber glow
  } else if (highlightState === 'downstream') {
    borderColor = 'border-red-500'; // Red for downstream
    glowEffect = 'shadow-[0_0_10px_rgba(239,68,68,0.5)]'; // Red glow
  }

  if (isOrigin) {
    borderColor = 'border-purple-500';
    glowEffect = 'shadow-[0_0_15px_rgba(168,85,247,0.7)]';
    opacity = 'opacity-100'; // Ensure origin is never dimmed
  }

  return (
    <div
      className={`min-w-[180px] p-4 rounded-xl border-2 transition-all duration-300 ${bgColor} ${borderColor} ${textColor} ${opacity} ${glowEffect} shadow-sm`}
    >
      <Handle type="target" position={Position.Top} className="w-2 h-2 !bg-slate-400" />

      <div className="flex items-center gap-2 mb-2">
        <Icon className="w-4 h-4" />
        <span className="text-xs font-semibold uppercase tracking-wider opacity-80">{typeLabel}</span>
      </div>

      <div className="font-semibold text-sm mb-1 truncate">{label}</div>

      {impact && (
        <div className="mt-3">
          <Badge
            variant={impact.total_score >= 80 ? "destructive" : impact.total_score >= 50 ? "default" : "secondary"}
            className={impact.total_score >= 80 ? "bg-red-500 hover:bg-red-600 text-white" : impact.total_score >= 50 ? "bg-amber-500 hover:bg-amber-600 text-white" : "bg-slate-200 text-slate-700"}
          >
            Impact: {impact.total_score}
          </Badge>
        </div>
      )}

      {data.onAnalyzeImpact && !isOrigin && highlightState === 'none' && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            data.onAnalyzeImpact!(data.nodeId);
          }}
          className="mt-3 text-xs w-full py-1 px-2 rounded bg-white/10 hover:bg-white/20 border border-white/20 transition-colors"
          style={type !== 'ai_system' ? { backgroundColor: 'rgba(0,0,0,0.05)', borderColor: 'rgba(0,0,0,0.1)', color: 'black' } : {}}
        >
          Analyze Impact
        </button>
      )}

      {isOrigin && (
        <div className="mt-2 text-xs font-bold text-purple-400">
          Origin Node
        </div>
      )}

      <Handle type="source" position={Position.Bottom} className="w-2 h-2 !bg-slate-400" />
    </div>
  );
};

export default CustomNode;