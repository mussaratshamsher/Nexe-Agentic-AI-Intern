import { WorkflowVisualizer } from "@/components/dashboard/WorkflowVisualizer";
import { Zap, Activity, Cpu, Share2 } from "lucide-react";

export default function WorkflowPage() {
  return (
    <div className="max-w-7xl mx-auto p-4 md:p-8 space-y-8 animate-in fade-in duration-700">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div className="space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-bold uppercase tracking-widest">
            <Activity className="w-3 h-3" />
            Live System Monitoring
          </div>
          <h1 className="text-4xl md:text-6xl font-black tracking-tighter text-white uppercase italic">
            Neural Pathways
          </h1>
          <p className="text-muted-foreground max-w-2xl text-lg font-medium leading-relaxed">
            Visualize how the Master Orchestrator processes your requests and delegates complex tasks to specialized agents across the platform.
          </p>
        </div>
        
        <div className="flex gap-4">
          <div className="px-6 py-3 bg-card border border-border rounded-2xl flex items-center gap-3">
            <Cpu className="w-5 h-5 text-primary" />
            <div>
              <p className="text-[10px] font-black text-muted-foreground uppercase tracking-widest">System Load</p>
              <p className="text-sm font-bold text-white uppercase">Optimal</p>
            </div>
          </div>
          <div className="px-6 py-3 bg-card border border-border rounded-2xl flex items-center gap-3">
            <Share2 className="w-5 h-5 text-primary" />
            <div>
              <p className="text-[10px] font-black text-muted-foreground uppercase tracking-widest">Active Links</p>
              <p className="text-sm font-bold text-white uppercase">05 Channels</p>
            </div>
          </div>
        </div>
      </div>

      <WorkflowVisualizer />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          { 
            title: "Dynamic Delegation", 
            desc: "The Orchestrator automatically selects agents based on intent analysis and available tools.",
            icon: Zap 
          },
          { 
            title: "Inter-Agent Comms", 
            desc: "Agents share context and results to synthesize complex responses without human intervention.",
            icon: Share2 
          },
          { 
            title: "Neural Synthesis", 
            desc: "Final outputs are formatted based on channel-specific guidelines and style requirements.",
            icon: Cpu 
          }
        ].map((item, i) => (
          <div key={i} className="p-8 rounded-[2rem] bg-secondary/10 border border-border hover:border-primary/30 transition-all">
            <item.icon className="w-8 h-8 text-primary mb-4" />
            <h4 className="text-lg font-black text-white uppercase italic mb-2">{item.title}</h4>
            <p className="text-sm text-muted-foreground leading-relaxed">{item.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
