"use client";

import { motion } from "framer-motion";
import { 
  Target, 
  TrendingUp, 
  Users, 
  ArrowUpRight, 
  Zap, 
  MessageSquare,
  Search,
  Filter,
  MoreVertical
} from "lucide-react";
import { useState, useEffect } from "react";
import { CommandCenterCard } from "@/components/ui/command-center-card";
import { customerService, Customer } from "@/services/customer.service";

export default function CRMPage() {
  const [query, setQuery] = useState("");
  const [customers, setCustomers] = useState<Customer[]>([]);

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const data = await customerService.getCustomers();
        setCustomers(data);
      } catch (err) {
        console.error("Error fetching customers:", err);
      }
    };
    fetchCustomers();
  }, []);

  return (
    <div className="max-w-7xl mx-auto p-4 md:p-8 space-y-10 animate-in fade-in duration-700">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div className="space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 text-xs font-bold uppercase tracking-widest">
            <Target className="w-3 h-3" />
            AI Lead Intelligence Active
          </div>
          <h1 className="text-4xl md:text-6xl font-black tracking-tighter text-white uppercase italic">
            Command CRM
          </h1>
          <p className="text-muted-foreground max-w-2xl text-lg font-medium leading-relaxed">
            Our AI agents analyze customer sentiment, score leads, and identify high-value opportunities automatically.
          </p>
        </div>
        
        <div className="flex gap-4">
          <div className="relative group">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground group-focus-within:text-primary transition-colors" />
            <input 
              type="text" 
              placeholder="Search Intelligence..."
              className="pl-10 pr-4 py-3 bg-card border border-border rounded-2xl text-sm font-bold uppercase italic tracking-tight focus:border-primary outline-none transition-all w-64"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>
          <button className="p-3 bg-card border border-border rounded-2xl hover:border-primary transition-all">
            <Filter className="w-5 h-5 text-muted-foreground" />
          </button>
        </div>
      </div>

      {/* Intelligence Stats (Kept as design placeholders as backend doesn't have aggregate endpoints yet) */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <CommandCenterCard glow="green">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-black text-muted-foreground uppercase tracking-[0.2em]">Total Value</h3>
            <TrendingUp className="w-4 h-4 text-emerald-400 opacity-50" />
          </div>
          <p className="text-4xl font-black mt-4 text-white italic tracking-tighter">$215.6K</p>
        </CommandCenterCard>
        
        <CommandCenterCard glow="blue">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-black text-muted-foreground uppercase tracking-[0.2em]">Lead Score</h3>
            <Zap className="w-4 h-4 text-primary opacity-50" />
          </div>
          <p className="text-4xl font-black mt-4 text-white italic tracking-tighter">88/100</p>
        </CommandCenterCard>

        <CommandCenterCard glow="purple">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-black text-muted-foreground uppercase tracking-[0.2em]">Sentiment</h3>
            <MessageSquare className="w-4 h-4 text-purple-400 opacity-50" />
          </div>
          <p className="text-4xl font-black mt-4 text-white italic tracking-tighter">92%</p>
        </CommandCenterCard>

        <CommandCenterCard glow="white">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-black text-muted-foreground uppercase tracking-[0.2em]">Conversions</h3>
            <Users className="w-4 h-4 text-white opacity-50" />
          </div>
          <p className="text-4xl font-black mt-4 text-white italic tracking-tighter">24</p>
        </CommandCenterCard>
      </div>

      {/* Intelligence Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main List */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-black uppercase italic text-white tracking-tight border-l-4 border-primary pl-4">Priority Intelligence</h2>
          </div>
          
          <div className="space-y-4">
            {customers.length > 0 ? customers.map((customer) => (
              <motion.div
                key={customer.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="p-6 rounded-3xl bg-card border border-border hover:border-primary/50 transition-all group flex items-center justify-between"
              >
                <div className="flex items-center gap-6">
                  <div className="w-12 h-12 rounded-2xl bg-secondary flex items-center justify-center text-xl font-black text-primary italic">
                    {customer.name[0]}
                  </div>
                  <div>
                    <h4 className="text-lg font-black text-white uppercase italic tracking-tight">{customer.name}</h4>
                    <div className="flex items-center gap-3 mt-1">
                      <span className={`text-[10px] font-black uppercase tracking-widest ${
                        customer.sentiment === 'Positive' ? 'text-emerald-400' : 
                        customer.sentiment === 'Negative' ? 'text-red-400' : 'text-yellow-400'
                      }`}>
                        {customer.sentiment} Sentiment
                      </span>
                      <span className="text-[10px] text-muted-foreground font-bold uppercase tracking-widest">•</span>
                      <span className="text-[10px] text-muted-foreground font-bold uppercase tracking-widest">{customer.last_activity}</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-12">
                  <div className="text-right">
                    <p className="text-[10px] font-black text-muted-foreground uppercase tracking-widest mb-1">Lead Score</p>
                    <div className="flex items-center gap-2">
                      <div className="w-24 h-1.5 bg-secondary rounded-full overflow-hidden">
                        <div 
                          className={`h-full ${customer.score > 80 ? 'bg-emerald-400' : customer.score > 50 ? 'bg-yellow-400' : 'bg-red-400'}`} 
                          style={{ width: `${customer.score}%` }}
                        />
                      </div>
                      <span className="text-sm font-black text-white italic">{customer.score}</span>
                    </div>
                  </div>
                  
                  <div className="text-right hidden md:block">
                    <p className="text-[10px] font-black text-muted-foreground uppercase tracking-widest mb-1">Deal Value</p>
                    <p className="text-lg font-black text-white italic">{customer.value}</p>
                  </div>

                  <button className="p-2 hover:bg-secondary rounded-xl transition-colors">
                    <MoreVertical className="w-5 h-5 text-muted-foreground" />
                  </button>
                </div>
              </motion.div>
            )) : (
                <div className="text-center py-20 text-muted-foreground font-black italic uppercase">No Intelligence Data Found</div>
            )}
          </div>
        </div>

        {/* AI Recommendations */}
        <div className="space-y-6">
          <h2 className="text-xl font-black uppercase italic text-white tracking-tight border-l-4 border-purple-400 pl-4">AI Recommendations</h2>
          <div className="space-y-4">
            {[
              { title: "High Urgency", desc: "High intent signals detected. Trigger Sales Agent.", color: "border-emerald-500/30" },
              { title: "Churn Risk", desc: "Sentiment dropping. PM Agent should schedule sync.", color: "border-red-500/30" },
              { title: "Expansion", desc: "Usage exceeded. Content Agent to draft proposal.", color: "border-purple-500/30" },
            ].map((rec, i) => (
              <div key={i} className={`p-6 rounded-3xl bg-secondary/10 border ${rec.color} space-y-3`}>
                <div className="flex items-center gap-2">
                  <Zap className="w-4 h-4 text-primary" />
                  <span className="text-xs font-black uppercase italic text-white">{rec.title}</span>
                </div>
                <p className="text-xs text-muted-foreground font-medium leading-relaxed">{rec.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
