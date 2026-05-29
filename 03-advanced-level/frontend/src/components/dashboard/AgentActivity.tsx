"use client";

import { motion, AnimatePresence } from "framer-motion";
import { 
  Bot, 
  Target, 
  ShieldCheck, 
  Clock, 
  MessageSquareCode,
  Zap
} from "lucide-react";
import { useState, useEffect } from "react";
import { executionService, ExecutionLog } from "@/services/execution.service";

interface Agent {
  name: string;
  icon: React.ElementType;
  color: string;
}

interface Task {
  id: number;
  agent: Agent;
  task: string;
  timestamp: string;
  status: string;
}

const agentIcons: Record<string, React.ElementType> = {
  'Sales Agent': Target,
  'Support Agent': ShieldCheck,
  'PM Agent': Clock,
  'Content Agent': MessageSquareCode,
};

const agentColors: Record<string, string> = {
  'Sales Agent': 'text-emerald-400',
  'Support Agent': 'text-blue-400',
  'PM Agent': 'text-orange-400',
  'Content Agent': 'text-pink-400',
};

export function AgentActivity() {
  const [activeTasks, setActiveTasks] = useState<Task[]>([]);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const logs = await executionService.getLogs();
        const mappedTasks = logs.map((log: ExecutionLog) => ({
          id: log.id,
          agent: {
            name: log.agent_name,
            icon: agentIcons[log.agent_name] || Bot,
            color: agentColors[log.agent_name] || 'text-white'
          },
          task: log.action,
          timestamp: new Date(log.created_at).toLocaleTimeString(),
          status: log.status
        }));
        setActiveTasks(mappedTasks.slice(0, 5));
      } catch (err) {
        console.error("Error fetching logs:", err);
      }
    };

    fetchLogs();
    const interval = setInterval(fetchLogs, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Bot className="w-5 h-5 text-primary" />
          <h3 className="text-sm font-black uppercase italic text-white tracking-tight">Active Workforce</h3>
        </div>
        <div className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
          <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-[10px] font-black uppercase text-emerald-500 tracking-widest">{activeTasks.length} Agents Online</span>
        </div>
      </div>

      <div className="space-y-3">
        <AnimatePresence mode="popLayout">
          {activeTasks.map((task, index) => (
            <motion.div
              key={task.id}
              layout
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{
                layout: { type: "spring", stiffness: 200, damping: 25 },
                opacity: { duration: 0.4 },
                y: { type: "spring", stiffness: 300, damping: 30 }
              }}
              className={`p-4 rounded-2xl bg-card border ${index === 0 ? 'border-primary/50 shadow-[0_0_20px_rgba(var(--primary),0.15)]' : 'border-border'} group overflow-hidden`}
            >
              <div className="flex items-start gap-4">
                <div className={`p-2 rounded-xl bg-secondary ${task.agent.color}`}>
                  <task.agent.icon className="w-5 h-5" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <h4 className="text-xs font-black uppercase text-white tracking-tight italic">
                      {task.agent.name}
                    </h4>
                    <span className="text-[10px] text-muted-foreground font-bold">{task.timestamp}</span>
                  </div>
                  <p className="text-xs text-muted-foreground font-medium truncate group-hover:text-white transition-colors">
                    {task.task}
                  </p>
                  <div className="mt-3 flex items-center gap-2">
                    <div className="flex-1 h-1 bg-secondary rounded-full overflow-hidden">
                      <motion.div 
                        initial={{ width: "0%" }}
                        animate={{ width: "100%" }}
                        transition={{ duration: 4, ease: "linear" }}
                        className="h-full bg-primary"
                      />
                    </div>
                    <span className="text-[10px] font-black uppercase text-primary tracking-widest">{task.status}</span>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {activeTasks.length === 0 && (
          <div className="py-12 flex flex-col items-center justify-center border border-dashed border-border rounded-3xl opacity-50">
            <Zap className="w-8 h-8 text-muted-foreground mb-3" />
            <p className="text-xs font-black uppercase tracking-widest text-muted-foreground">Waiting for orchestration...</p>
          </div>
        )}
      </div>
    </div>
  );
}
