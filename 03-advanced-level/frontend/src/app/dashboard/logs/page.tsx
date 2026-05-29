"use client";

import { motion, AnimatePresence } from "framer-motion";
import { 
  Terminal, 
  Cpu, 
  Zap, 
  Search, 
  Filter, 
  ChevronDown, 
  ChevronRight,
  ShieldCheck,
  Target,
  Clock,
  MessageSquareCode,
  Activity
} from "lucide-react";
import { useState, useEffect } from "react";

const agents = [
  { id: 'sales', name: 'Sales Agent', icon: Target, color: 'text-emerald-400' },
  { id: 'support', name: 'Support Agent', icon: ShieldCheck, color: 'text-blue-400' },
  { id: 'pm', name: 'PM Agent', icon: Clock, color: 'text-orange-400' },
  { id: 'content', name: 'Content Agent', icon: MessageSquareCode, color: 'text-pink-400' },
  { id: 'orchestrator', name: 'Orchestrator', icon: Zap, color: 'text-primary' },
];

const logData = [
  {
    id: "wf-1",
    timestamp: "10:24:05",
    agent: agents[4],
    event: "Workflow Initiated",
    details: "Analyzing user request: 'Need a proposal for Acme Corp project expansion.'",
    status: "success",
    trace: [
      { timestamp: "10:24:06", msg: "Parsing intent: CONTENT_GENERATION", status: "info" },
      { timestamp: "10:24:08", msg: "Delegating to Sales Agent for CRM data", status: "success" },
      { timestamp: "10:24:10", msg: "Delegating to PM Agent for timeline", status: "success" },
    ]
  },
  {
    id: "wf-2",
    timestamp: "10:25:12",
    agent: agents[0],
    event: "CRM Intelligence Retrieval",
    details: "Fetching Acme Corp history and current deal status from CRM.",
    status: "success",
    trace: [
      { timestamp: "10:25:13", msg: "Connecting to CRM Node...", status: "info" },
      { timestamp: "10:25:15", msg: "Retrieved 12 historical records", status: "success" },
      { timestamp: "10:25:18", msg: "Calculated lead score: 95/100", status: "success" },
    ]
  },
  {
    id: "wf-3",
    timestamp: "10:26:45",
    agent: agents[2],
    event: "Timeline Generation",
    details: "Synthesizing project milestones based on historical delivery speed.",
    status: "success",
    trace: [
      { timestamp: "10:26:46", msg: "Analyzing team capacity", status: "info" },
      { timestamp: "10:26:50", msg: "Milestones generated: 5 key dates", status: "success" },
    ]
  },
  {
    id: "wf-4",
    timestamp: "10:28:10",
    agent: agents[3],
    event: "Proposal Synthesis",
    details: "Drafting final project proposal with integrated sales and PM data.",
    status: "executing",
    trace: [
      { timestamp: "10:28:11", msg: "Formatting for Professional PDF", status: "info" },
      { timestamp: "10:28:15", msg: "Applying brand guidelines", status: "info" },
      { timestamp: "10:28:20", msg: "Generating content blocks...", status: "executing" },
    ]
  }
];

export default function LogsPage() {
  const [expandedId, setExpandedId] = useState<string | null>("wf-4");
  const [filter, setFilter] = useState("all");

  return (
    <div className="max-w-7xl mx-auto p-4 md:p-8 space-y-10 animate-in fade-in duration-700">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div className="space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-bold uppercase tracking-widest">
            <Terminal className="w-3 h-3" />
            Neural Trace Interface Online
          </div>
          <h1 className="text-4xl md:text-6xl font-black tracking-tighter text-white uppercase italic">
            Agent Logs
          </h1>
          <p className="text-muted-foreground max-w-2xl text-lg font-medium leading-relaxed">
            Deep-dive into the autonomous execution traces of your digital workforce.
          </p>
        </div>
        
        <div className="flex gap-4">
          <div className="flex p-1 bg-secondary/30 border border-border rounded-2xl">
            {["all", "success", "errors", "active"].map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${
                  filter === f ? 'bg-primary text-primary-foreground shadow-lg' : 'text-muted-foreground hover:text-white'
                }`}
              >
                {f}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Real-time Monitor */}
      <div className="grid grid-cols-1 gap-6">
        <div className="rounded-[2.5rem] bg-black border border-border/50 overflow-hidden shadow-2xl">
          <div className="bg-secondary/20 border-b border-border px-8 py-4 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="flex gap-1.5">
                <div className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/50" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/50" />
                <div className="w-3 h-3 rounded-full bg-emerald-500/20 border border-emerald-500/50" />
              </div>
              <span className="text-[10px] font-black uppercase tracking-[0.3em] text-muted-foreground">Neural Execution Monitor v4.0</span>
            </div>
            <div className="flex items-center gap-2">
              <Activity className="w-3 h-3 text-emerald-500 animate-pulse" />
              <span className="text-[10px] font-black uppercase tracking-widest text-emerald-500">System Live</span>
            </div>
          </div>

          <div className="p-4 md:p-8 space-y-4 max-h-[800px] overflow-y-auto font-mono">
            {logData.map((log) => (
              <div key={log.id} className="space-y-2">
                <button
                  onClick={() => setExpandedId(expandedId === log.id ? null : log.id)}
                  className={`w-full flex items-start gap-4 p-4 rounded-2xl border transition-all text-left ${
                    expandedId === log.id 
                      ? 'bg-secondary/20 border-primary/50' 
                      : 'bg-transparent border-border/20 hover:border-border/50'
                  }`}
                >
                  <div className="mt-1">
                    {expandedId === log.id ? <ChevronDown className="w-4 h-4 text-primary" /> : <ChevronRight className="w-4 h-4 text-muted-foreground" />}
                  </div>
                  <div className="flex-1 space-y-2">
                    <div className="flex flex-wrap items-center gap-3">
                      <span className="text-xs text-muted-foreground">[{log.timestamp}]</span>
                      <div className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-widest bg-secondary ${log.agent.color}`}>
                        {log.agent.name}
                      </div>
                      <span className="text-sm font-bold text-white uppercase italic tracking-tight">{log.event}</span>
                      {log.status === 'executing' && (
                        <span className="flex items-center gap-1.5 px-2 py-0.5 rounded bg-primary/10 text-primary text-[10px] font-black uppercase animate-pulse">
                          Executing
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-muted-foreground leading-relaxed">{log.details}</p>
                  </div>
                </button>

                <AnimatePresence>
                  {expandedId === log.id && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="overflow-hidden ml-8 border-l border-border/30"
                    >
                      <div className="py-2 space-y-1">
                        {log.trace.map((t, i) => (
                          <div key={i} className="flex items-center gap-4 py-1.5 px-4 hover:bg-secondary/10 transition-colors group">
                            <span className="text-[10px] text-muted-foreground/50 w-20">[{t.timestamp}]</span>
                            <div className={`w-1.5 h-1.5 rounded-full ${
                              t.status === 'success' ? 'bg-emerald-500' : 
                              t.status === 'executing' ? 'bg-primary animate-pulse' : 'bg-blue-400'
                            }`} />
                            <span className={`text-[11px] font-medium ${t.status === 'executing' ? 'text-primary' : 'text-muted-foreground group-hover:text-white'}`}>
                              {t.msg}
                            </span>
                          </div>
                        ))}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ))}
          </div>
          
          <div className="bg-secondary/20 border-t border-border px-8 py-4 flex items-center justify-between">
            <div className="flex items-center gap-6">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-emerald-500" />
                <span className="text-[10px] font-black text-muted-foreground uppercase tracking-widest">Success: 98.4%</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-primary" />
                <span className="text-[10px] font-black text-muted-foreground uppercase tracking-widest">Active: 01</span>
              </div>
            </div>
            <button className="text-[10px] font-black uppercase tracking-widest text-primary hover:text-white transition-colors">
              Clear History
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
