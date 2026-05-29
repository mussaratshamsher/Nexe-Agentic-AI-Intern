"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { toast } from "sonner";
import { Settings, Shield, MessageSquare, Mail, Hash, Smartphone, Key, Bell } from "lucide-react";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function ManageAccountPage() {
  const [password, setPassword] = useState("");

  const handleUpdatePassword = () => {
    toast.success("Password updated successfully.");
    setPassword("");
  };

  return (
    <div className="max-w-4xl mx-auto p-4 md:p-8 space-y-10 animate-in fade-in duration-700">
      <div className="space-y-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-bold uppercase tracking-widest">
          <Settings className="w-3 h-3" />
          System Configuration
        </div>
        <h1 className="text-4xl md:text-6xl font-black tracking-tighter text-white uppercase italic">
          Account Control
        </h1>
        <p className="text-muted-foreground max-w-2xl text-lg font-medium leading-relaxed">
          Manage your personal profile, security settings, and agent connectivity across multiple communication channels.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Card className="bg-card border-border rounded-[2.5rem] overflow-hidden">
          <CardHeader className="p-8 border-b border-border bg-secondary/10">
            <CardTitle className="text-xl font-black uppercase italic tracking-tight flex items-center gap-3">
              <Shield className="w-5 h-5 text-primary" />
              Security Core
            </CardTitle>
            <CardDescription className="text-[10px] font-bold uppercase tracking-widest">Update your access credentials</CardDescription>
          </CardHeader>
          <CardContent className="p-8 space-y-6">
            <div className="flex items-center gap-6">
              <div className="w-20 h-20 rounded-[2rem] bg-gradient-to-br from-primary/20 to-primary/5 border border-primary/20 flex items-center justify-center text-3xl font-black text-primary italic shadow-lg">
                JD
              </div>
              <div className="space-y-1">
                <p className="text-lg font-black text-white uppercase italic">John Doe</p>
                <p className="text-xs text-muted-foreground font-medium">john@example.com</p>
                <Button variant="link" className="p-0 h-auto text-[10px] font-black uppercase tracking-widest text-primary">Upload New Avatar</Button>
              </div>
            </div>
            
            <div className="space-y-4 pt-4">
              <div className="space-y-2">
                <label className="text-[10px] font-black uppercase tracking-widest text-muted-foreground">New Neural Key (Password)</label>
                <div className="relative">
                  <Key className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input 
                    type="password" 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••••••"
                    className="pl-12 h-12 rounded-xl bg-secondary/20 border-border focus:border-primary/50"
                  />
                </div>
              </div>
              <Button onClick={handleUpdatePassword} className="w-full h-12 rounded-xl font-black uppercase tracking-widest italic bg-primary shadow-xl shadow-primary/20">Update Security</Button>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-card border-border rounded-[2.5rem] overflow-hidden">
          <CardHeader className="p-8 border-b border-border bg-secondary/10">
            <CardTitle className="text-xl font-black uppercase italic tracking-tight flex items-center gap-3">
              <Bell className="w-5 h-5 text-primary" />
              Omnichannel Control
            </CardTitle>
            <CardDescription className="text-[10px] font-bold uppercase tracking-widest">Connect agents to external platforms</CardDescription>
          </CardHeader>
          <CardContent className="p-8 space-y-8">
            {[
              { name: 'Slack Integration', icon: Hash, status: 'Connected', active: true },
              { name: 'WhatsApp Bot', icon: Smartphone, status: 'Ready', active: false },
              { name: 'Email Gateway', icon: Mail, status: 'Active', active: true },
            ].map((item) => (
              <div key={item.name} className="flex items-center justify-between group">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-xl bg-secondary/50 flex items-center justify-center border border-border group-hover:border-primary/50 transition-colors">
                    <item.icon className="w-5 h-5 text-muted-foreground group-hover:text-primary transition-colors" />
                  </div>
                  <div>
                    <p className="text-sm font-black text-white uppercase italic tracking-tight">{item.name}</p>
                    <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">{item.status}</p>
                  </div>
                </div>
                <Switch checked={item.active} className="data-[state=checked]:bg-primary" />
              </div>
            ))}
            <div className="pt-4 p-4 rounded-2xl bg-primary/5 border border-primary/10">
              <p className="text-[10px] font-bold text-primary uppercase tracking-widest mb-1">Expert Note</p>
              <p className="text-[10px] text-muted-foreground leading-relaxed italic">
                Enabling a channel allows the Orchestrator to automatically respond to messages received via that platform using your configured agent workforce.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
