"use client";
import React, { useCallback, useMemo } from 'react';
import { motion } from "framer-motion";
import ReactFlow, { 
  Node,
  Background, 
  Controls, 
  MiniMap,
  useNodesState,
  useEdgesState,
  addEdge,
  Handle,
  Position,
  Connection,
  Edge,
  MarkerType
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Bot, Zap, ShieldCheck, Target, MessageSquareCode, Clock } from 'lucide-react';

interface AgentData {
  label: string;
  role: React.ElementType;
  icon: React.ElementType;
  color: string;
  isActive: boolean;
  reasoning?: string;
}

const AgentNode = ({ data }: { data: AgentData }) => {
  const Icon = data.icon || Bot;
  return (
    <div className={`px-6 py-4 rounded-2xl bg-card border-2 ${data.isActive ? 'border-primary shadow-[0_0_20px_rgba(var(--primary),0.3)] scale-105' : 'border-border'} transition-all min-w-[220px] relative group`}>
      <Handle type="target" position={Position.Top} className="w-3 h-3 bg-primary" />
      
      {data.isActive && (
        <div className="absolute -top-2 -right-2 w-4 h-4 rounded-full bg-primary animate-ping" />
      )}

      <div className="flex items-center gap-3">
        <div className={`p-2.5 rounded-xl bg-secondary ${data.color} shadow-sm group-hover:scale-110 transition-transform`}>
          <Icon className="w-6 h-6" />
        </div>
        <div>
          <h4 className="text-sm font-black uppercase italic text-white tracking-tight">{data.label}</h4>
          <p className="text-[10px] text-muted-foreground font-bold uppercase tracking-widest">{data.role as unknown as string}</p>
        </div>
      </div>
      {data.reasoning && (
        <div className="mt-3 pt-3 border-t border-border/50">
          <p className="text-[10px] text-primary/80 font-medium italic leading-relaxed">
            &quot;{data.reasoning}&quot;
          </p>
        </div>
      )}
      
      <div className="mt-4 flex items-center gap-2">
        <div className="flex-1 h-1 bg-secondary rounded-full overflow-hidden">
          <motion.div 
            initial={{ width: "0%" }}
            animate={{ width: data.isActive ? "100%" : "0%" }}
            transition={{ duration: 2, repeat: Infinity }}
            className="h-full bg-primary"
          />
        </div>
        <span className="text-[8px] font-black uppercase text-primary tracking-widest">{data.isActive ? 'Active' : 'Idle'}</span>
      </div>

      <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-primary" />
    </div>
  );
};

const nodeTypes = {
  agent: AgentNode,
};

const initialNodes = [
  {
    id: 'orchestrator',
    type: 'agent',
    position: { x: 250, y: 0 },
    data: { 
      label: 'Master Orchestrator', 
      role: 'Neural Core', 
      icon: Zap, 
      color: 'text-primary',
      isActive: true,
      reasoning: 'Analyzing request and delegating to specialized agents.'
    },
  },
  {
    id: 'sales',
    type: 'agent',
    position: { x: 0, y: 150 },
    data: { 
      label: 'Sales Agent', 
      role: 'Lead Qualification', 
      icon: Target, 
      color: 'text-emerald-400',
      isActive: false,
      reasoning: 'Qualifying lead based on budget and intent.'
    },
  },
  {
    id: 'support',
    type: 'agent',
    position: { x: 250, y: 150 },
    data: { 
      label: 'Support Agent', 
      role: 'Customer Success', 
      icon: ShieldCheck, 
      color: 'text-blue-400',
      isActive: false,
      reasoning: 'Searching knowledge base for technical resolution.'
    },
  },
  {
    id: 'pm',
    type: 'agent',
    position: { x: 500, y: 150 },
    data: { 
      label: 'PM Agent', 
      role: 'Project Logistics', 
      icon: Clock, 
      color: 'text-orange-400',
      isActive: false,
      reasoning: 'Drafting project timeline and milestones.'
    },
  },
  {
    id: 'content',
    type: 'agent',
    position: { x: 250, y: 300 },
    data: { 
      label: 'Content Agent', 
      role: 'Creative Engine', 
      icon: MessageSquareCode, 
      color: 'text-pink-400',
      isActive: false,
      reasoning: 'Synthesizing final proposal from agent outputs.'
    },
  },
];

const initialEdges = [
  { id: 'e-o-s', source: 'orchestrator', target: 'sales', animated: true, markerEnd: { type: MarkerType.ArrowClosed, color: '#facc15' } },
  { id: 'e-o-sup', source: 'orchestrator', target: 'support', animated: true, markerEnd: { type: MarkerType.ArrowClosed, color: '#60a5fa' } },
  { id: 'e-o-pm', source: 'orchestrator', target: 'pm', animated: true, markerEnd: { type: MarkerType.ArrowClosed, color: '#fb923c' } },
  { id: 'e-s-c', source: 'sales', target: 'content', animated: true },
  { id: 'e-sup-c', source: 'support', target: 'content', animated: true },
  { id: 'e-pm-c', source: 'pm', target: 'content', animated: true },
];

export function WorkflowVisualizer() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  return (
    <div className="w-full h-[600px] bg-secondary/20 rounded-[2rem] border border-border/50 overflow-hidden relative group">
      <div className="absolute top-6 left-6 z-10 flex flex-col gap-2">
        <h3 className="text-xl font-black uppercase italic text-white tracking-tighter">Neural Workflow</h3>
        <p className="text-xs text-muted-foreground font-bold uppercase tracking-widest">Real-time Agent Orchestration</p>
      </div>
      
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitView
        className="bg-dot-pattern"
      >
        <Background color="#333" gap={20} />
        <Controls className="!bg-card !border-border !fill-white" />
        <MiniMap 
          className="!bg-card !border-border"
          nodeColor={(n: Node) => {
            if (n.id === 'orchestrator') return '#facc15';
            return '#333';
          }}
        />
      </ReactFlow>
    </div>
  );
}
