"use client";
import { useState } from "react";
import { 
  Ticket, 
  ShieldCheck, 
  AlertCircle, 
  Clock, 
  Search, 
  Filter, 
  MoreVertical,
  Zap,
  CheckCircle2,
  Bot
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardHeader, 
  CardTitle 
} from "@/components/ui/card";

const initialTickets = [
  { id: "TK-101", subject: "Unable to access API key", customer: "John Doe", priority: "High", status: "Open", autopilot: true, draft: "I've checked your account and it seems..." },
  { id: "TK-102", subject: "Billing discrepancy", customer: "Jane Smith", priority: "Medium", status: "Open", autopilot: false, draft: null },
  { id: "TK-103", subject: "New feature request", customer: "Bob Wilson", priority: "Low", status: "Closed", autopilot: false, draft: null },
];

export default function TicketsPage() {
  const [tickets, setTickets] = useState(initialTickets);

  const toggleAutopilot = (id: string) => {
    setTickets(tickets.map(t => t.id === id ? { ...t, autopilot: !t.autopilot } : t));
  };

  return (
    <div className="max-w-7xl mx-auto p-4 md:p-8 space-y-10 animate-in fade-in duration-700">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div className="space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-bold uppercase tracking-widest">
            <ShieldCheck className="w-3 h-3" />
            Customer Success Engine
          </div>
          <h1 className="text-4xl md:text-6xl font-black tracking-tighter text-white uppercase italic">
            Ticket Command
          </h1>
          <p className="text-muted-foreground max-w-2xl text-lg font-medium leading-relaxed">
            Manage your support queue with AI Auto-Pilot. Enable &apos;Auto-Pilot&apos; on tickets to let the Support Agent draft resolutions based on your knowledge base.
          </p>
        </div>
      </div>

      <div className="flex flex-wrap gap-4 items-center justify-between">
        <div className="flex gap-4 flex-1 min-w-[300px]">
          <div className="relative flex-1">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input placeholder="Search tickets..." className="pl-11 rounded-2xl bg-card border-border" />
          </div>
          <Button variant="outline" className="rounded-2xl gap-2 font-bold uppercase text-[10px] tracking-widest border-border">
            <Filter className="w-4 h-4" />
            Filter
          </Button>
        </div>
        <div className="flex items-center gap-3 px-4 py-2 bg-primary/5 border border-primary/20 rounded-2xl">
          <Bot className="w-4 h-4 text-primary" />
          <span className="text-[10px] font-black uppercase tracking-widest text-white">Global Auto-Pilot</span>
          <Switch className="data-[state=checked]:bg-primary" />
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {tickets.map((t) => (
          <Card key={t.id} className="bg-card border-border hover:border-primary/30 transition-all rounded-[2rem] overflow-hidden group">
            <div className="flex flex-col md:flex-row">
              <div className="p-8 flex-1 space-y-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-xs font-black text-primary font-mono">{t.id}</span>
                    <Badge variant="outline" className={`
                      uppercase text-[9px] font-black tracking-widest rounded-lg border-none
                      ${t.priority === 'High' ? 'bg-destructive/10 text-destructive' : 
                        t.priority === 'Medium' ? 'bg-orange-400/10 text-orange-400' : 'bg-secondary text-muted-foreground'}
                    `}>
                      {t.priority}
                    </Badge>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                      <Zap className={`w-3 h-3 ${t.autopilot ? 'text-primary' : 'text-muted-foreground'}`} />
                      <span className="text-[9px] font-black uppercase tracking-widest text-muted-foreground">Auto-Pilot</span>
                      <Switch 
                        checked={t.autopilot} 
                        onCheckedChange={() => toggleAutopilot(t.id)}
                        className="data-[state=checked]:bg-primary scale-75"
                      />
                    </div>
                    <Button variant="ghost" size="icon" className="rounded-xl"><MoreVertical className="w-4 h-4" /></Button>
                  </div>
                </div>

                <div>
                  <h3 className="text-xl font-black text-white uppercase italic tracking-tight mb-1">{t.subject}</h3>
                  <p className="text-xs text-muted-foreground font-medium">Customer: <span className="text-white">{t.customer}</span></p>
                </div>

                {t.autopilot && t.draft && (
                  <div className="p-6 rounded-[1.5rem] bg-primary/5 border border-primary/10 space-y-3 relative group/draft">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2 text-primary">
                        <Bot className="w-4 h-4" />
                        <span className="text-[10px] font-black uppercase tracking-widest italic">AI Drafted Resolution</span>
                      </div>
                      <Badge className="bg-emerald-400/10 text-emerald-400 text-[8px] border-none">Ready for Review</Badge>
                    </div>
                    <p className="text-sm text-muted-foreground italic leading-relaxed">
                      &quot;{t.draft}&quot;
                    </p>
                    <div className="flex gap-3 pt-2">
                      <Button className="h-9 px-6 rounded-xl text-[10px] font-black uppercase tracking-widest italic bg-primary shadow-lg shadow-primary/20">Send Now</Button>
                      <Button variant="ghost" className="h-9 px-6 rounded-xl text-[10px] font-black uppercase tracking-widest">Edit Draft</Button>
                    </div>
                  </div>
                )}
              </div>

              <div className="md:w-64 bg-secondary/20 p-8 border-l border-border flex flex-col justify-between gap-6">
                <div className="space-y-4">
                  <div>
                    <p className="text-[10px] font-black text-muted-foreground uppercase tracking-widest mb-2">Status</p>
                    <div className="flex items-center gap-2">
                      <div className={`w-2 h-2 rounded-full ${t.status === 'Open' ? 'bg-primary' : 'bg-muted-foreground'}`} />
                      <span className="text-sm font-bold text-white uppercase">{t.status}</span>
                    </div>
                  </div>
                  <div>
                    <p className="text-[10px] font-black text-muted-foreground uppercase tracking-widest mb-2">Assigned Agent</p>
                    <div className="flex items-center gap-2">
                      <ShieldCheck className="w-4 h-4 text-primary" />
                      <span className="text-sm font-bold text-white uppercase tracking-tighter italic">Support_A1</span>
                    </div>
                  </div>
                </div>
                <Button variant="outline" className="w-full rounded-xl border-border hover:border-primary/50 text-xs font-bold uppercase italic">View Details</Button>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
