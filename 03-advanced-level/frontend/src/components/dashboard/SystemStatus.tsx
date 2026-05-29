"use client";

import { motion } from "framer-motion";
import { Activity, Cpu, Globe, Zap, Server, ShieldCheck } from "lucide-react";
import { useEffect, useState } from "react";

export function SystemStatus() {
  const [metrics, setMetrics] = useState({
    cpu: 12,
    memory: 45,
    latency: 85,
    success: 99.9
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => ({
        cpu: Math.max(5, Math.min(95, prev.cpu + (Math.random() * 10 - 5))),
        memory: Math.max(20, Math.min(80, prev.memory + (Math.random() * 4 - 2))),
        latency: Math.max(40, Math.min(200, prev.latency + (Math.random() * 20 - 10))),
        success: 99.9
      }));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <StatusCard 
        label="Neural Core" 
        value={`${Math.round(metrics.cpu)}%`} 
        icon={Cpu} 
        trend="stable"
        color="text-primary"
      />
      <StatusCard 
        label="System Latency" 
        value={`${Math.round(metrics.latency)}ms`} 
        icon={Zap} 
        trend="up"
        color="text-yellow-400"
      />
      <StatusCard 
        label="Uptime" 
        value="100%" 
        icon={ShieldCheck} 
        trend="stable"
        color="text-emerald-400"
      />
      <StatusCard 
        label="Active Nodes" 
        value="24/24" 
        icon={Server} 
        trend="stable"
        color="text-blue-400"
      />
    </div>
  );
}

interface StatusCardProps {
  label: string;
  value: string;
  icon: React.ElementType;
  trend: "stable" | "up" | "down";
  color: string;
}

function StatusCard({ label, value, icon: Icon, trend, color }: StatusCardProps) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-4 rounded-2xl bg-card/50 border border-border flex flex-col gap-2 relative overflow-hidden group"
    >
      <div className="flex items-center justify-between">
        <div className={`p-1.5 rounded-lg bg-secondary ${color}`}>
          <Icon className="w-4 h-4" />
        </div>
        <div className="flex items-center gap-1">
          <div className={`w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse`} />
          <span className="text-[10px] font-black uppercase text-emerald-500 tracking-widest">Live</span>
        </div>
      </div>
      <div>
        <p className="text-[10px] font-black text-muted-foreground uppercase tracking-widest">{label}</p>
        <p className="text-xl font-black text-white italic tracking-tight">{value}</p>
      </div>
      <div className="absolute -right-2 -bottom-2 w-12 h-12 opacity-5 group-hover:opacity-10 transition-opacity">
        <Icon className="w-full h-full" />
      </div>
    </motion.div>
  );
}
