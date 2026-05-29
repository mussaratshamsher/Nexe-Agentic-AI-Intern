"use client";

import { motion } from "framer-motion";
import { 
  Bot, 
  Users, 
  Ticket, 
  Zap, 
  ShieldCheck, 
  BarChart3, 
  MessageSquareCode, 
  Target,
  Clock,
  TrendingUp,
  Book,
  Settings,
  ArrowUpRight,
  Activity,
  Cpu,
  Globe
} from "lucide-react";
import Link from "next/link";
import { SystemStatus } from "@/components/dashboard/SystemStatus";
import { AgentActivity } from "@/components/dashboard/AgentActivity";
import { CommandCenterCard } from "@/components/ui/command-center-card";

export default function DashboardPage() {
  return (
    <div className="max-w-7xl mx-auto p-4 md:p-8 space-y-12 animate-in fade-in duration-700">
      {/* Hero Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-8">
        <div className="space-y-4">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-[10px] font-black uppercase tracking-[0.2em]"
          >
            <Activity className="w-3 h-3 animate-pulse" />
            Autonomous Workforce Online
          </motion.div>
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-5xl md:text-7xl font-black tracking-tighter text-white uppercase italic leading-none"
          >
            Command <span className="text-primary">Center</span>
          </motion.h1>
          <p className="text-muted-foreground max-w-2xl text-lg font-medium leading-relaxed">
            Orchestrating specialized autonomous agents to handle your business operations with zero human intervention.
          </p>
        </div>
        
        <div className="flex gap-4">
          <Link href="/dashboard/chat" className="px-8 py-4 bg-primary text-primary-foreground rounded-2xl font-black uppercase tracking-widest hover:scale-105 transition-all shadow-[0_0_20px_rgba(var(--primary),0.3)] italic">
            Initialize Workflow
          </Link>
        </div>
      </div>

      {/* Real-time System Status */}
      <div className="space-y-4">
        <div className="flex items-center gap-2 px-4 border-l-4 border-primary">
          <h2 className="text-sm font-black uppercase italic text-white tracking-[0.2em]">Infrastructure Monitor</h2>
        </div>
        <SystemStatus />
      </div>

      {/* Main Grid: Features & Live Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
        <div className="lg:col-span-2 space-y-10">
          {/* Quick Access */}
          <div className="space-y-6">
            <h2 className="text-xl md:text-2xl font-black tracking-tight uppercase italic border-l-4 border-primary pl-4">Neural Gateways</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                { title: "Neural Workflow", desc: "Visualize agent paths", href: "/dashboard/workflow", icon: Zap, color: "text-purple-400", glow: "purple" },
                { title: "Lead Intelligence", desc: "Predictive CRM scoring", href: "/dashboard/crm", icon: Target, color: "text-emerald-400", glow: "green" },
                { title: "Ticket Command", desc: "AI Support Auto-Pilot", href: "/dashboard/tickets", icon: ShieldCheck, color: "text-blue-400", glow: "blue" },
                { title: "Agent Tracing", desc: "Real-time execution logs", href: "/dashboard/logs", icon: Bot, color: "text-orange-400", glow: "white" },
              ].map((feat) => (
                <Link key={feat.title} href={feat.href}>
                  <div className="p-6 rounded-[2rem] bg-card border border-border hover:border-primary/50 transition-all group relative overflow-hidden flex items-center gap-6">
                    <div className={`p-4 rounded-2xl bg-secondary ${feat.color}`}>
                      <feat.icon className="w-8 h-8" />
                    </div>
                    <div>
                      <h4 className="text-xl font-black text-white uppercase tracking-tighter italic">{feat.title}</h4>
                      <p className="text-xs text-muted-foreground font-medium">{feat.desc}</p>
                    </div>
                    <ArrowUpRight className="w-5 h-5 ml-auto text-muted-foreground group-hover:text-primary transition-colors" />
                  </div>
                </Link>
              ))}
            </div>
          </div>

          {/* Efficiency Analytics */}
          <div className="space-y-6">
            <h2 className="text-xl md:text-2xl font-black tracking-tight uppercase italic border-l-4 border-primary pl-4">Optimization Metrics</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <CommandCenterCard glow="blue">
                <p className="text-[10px] font-black text-muted-foreground uppercase tracking-widest mb-2">Completion Rate</p>
                <p className="text-4xl font-black text-white italic tracking-tighter">99.2%</p>
                <div className="mt-4 h-1 w-full bg-secondary rounded-full overflow-hidden">
                  <div className="h-full bg-primary w-[99.2%]" />
                </div>
              </CommandCenterCard>
              <CommandCenterCard glow="purple">
                <p className="text-[10px] font-black text-muted-foreground uppercase tracking-widest mb-2">Avg Response</p>
                <p className="text-4xl font-black text-white italic tracking-tighter">1.4s</p>
                <p className="text-[10px] text-emerald-500 font-bold uppercase mt-2">⚡ Ultra Fast</p>
              </CommandCenterCard>
              <CommandCenterCard glow="green">
                <p className="text-[10px] font-black text-muted-foreground uppercase tracking-widest mb-2">Human Saved</p>
                <p className="text-4xl font-black text-white italic tracking-tighter">124h</p>
                <p className="text-[10px] text-muted-foreground font-bold uppercase mt-2">This Week</p>
              </CommandCenterCard>
            </div>
          </div>
        </div>

        {/* Live workforce activity */}
        <div className="space-y-6">
          <h2 className="text-xl md:text-2xl font-black tracking-tight uppercase italic border-l-4 border-emerald-400 pl-4">Live Activity</h2>
          <AgentActivity />
        </div>
      </div>

      {/* Bottom Workforce Breakdown */}
      <div className="space-y-8 py-10 border-t border-border/50">
        <h2 className="text-3xl font-black tracking-tighter uppercase italic text-white">The <span className="text-primary">Workforce</span></h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            { name: 'Sales Agent', role: 'Lead Qualification', icon: Target, color: 'text-emerald-400', status: 'Optimal' },
            { name: 'Support Agent', role: 'Customer Success', icon: ShieldCheck, color: 'text-blue-400', status: 'Active' },
            { name: 'PM Agent', role: 'Project Logistics', icon: Clock, color: 'text-orange-400', status: 'Active' },
            { name: 'Content Agent', role: 'Creative Engine', icon: MessageSquareCode, color: 'text-pink-400', status: 'Optimal' }
          ].map((agent) => (
            <div key={agent.name} className="p-6 rounded-3xl bg-card border border-border hover:border-primary/50 transition-all group relative overflow-hidden">
              <div className="flex items-center justify-between mb-4">
                <div className={`p-2 rounded-xl bg-secondary ${agent.color}`}>
                  <agent.icon className="w-6 h-6" />
                </div>
                <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
                  <div className="w-1 h-1 rounded-full bg-emerald-500 animate-pulse" />
                  <span className="text-[8px] font-black uppercase text-emerald-500 tracking-widest">{agent.status}</span>
                </div>
              </div>
              <h4 className="font-black text-white uppercase tracking-tight italic">{agent.name}</h4>
              <p className="text-[10px] font-bold text-primary uppercase tracking-[0.2em] mb-2">{agent.role}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
