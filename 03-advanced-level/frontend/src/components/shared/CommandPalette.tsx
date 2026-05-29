"use client";

import * as React from "react";
import {
  Calculator,
  Calendar,
  CreditCard,
  Settings,
  Smile,
  User,
  Search,
  Bot,
  Zap,
  Ticket,
  Users,
  MessageSquare,
  Activity,
  SearchIcon,
  Command as CommandIcon,
  Home
} from "lucide-react";
import { useRouter } from "next/navigation";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

export function CommandPalette() {
  const [open, setOpen] = React.useState(false);
  const [query, setQuery] = React.useState("");
  const router = useRouter();

  React.useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };

    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  const items = [
    {
      group: "Navigation",
      items: [
        { label: "Home", icon: Home, href: "/" },
        { label: "Dashboard", icon: Activity, href: "/dashboard" },
        { label: "Agent Chat", icon: MessageSquare, href: "/dashboard/chat" },
        { label: "Neural Workflow", icon: Zap, href: "/dashboard/workflow" },
        { label: "Lead Intelligence", icon: Users, href: "/dashboard/crm" },
        { label: "Ticket Command", icon: Ticket, href: "/dashboard/tickets" },
        { label: "Agent Logs", icon: Bot, href: "/dashboard/logs" },
      ]
    },
    {
      group: "Actions",
      items: [
        { label: "Search Customers", icon: Search, action: () => router.push("/dashboard/crm") },
        { label: "Trigger New Workflow", icon: Zap, action: () => router.push("/dashboard/workflow") },
        { label: "System Settings", icon: Settings, href: "/dashboard/account" },
      ]
    }
  ];

  const filteredItems = items.map(group => ({
    ...group,
    items: group.items.filter(item => 
      item.label.toLowerCase().includes(query.toLowerCase())
    )
  })).filter(group => group.items.length > 0);

  const runCommand = (command: () => void) => {
    setOpen(false);
    command();
  };

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-secondary/50 border border-border hover:border-primary/50 transition-all text-muted-foreground hover:text-white"
      >
        <Search className="w-4 h-4" />
        <span className="text-xs font-bold uppercase tracking-widest">Search...</span>
        <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100">
          <span className="text-xs">⌘</span>K
        </kbd>
      </button>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="max-w-2xl p-0 overflow-hidden bg-card border-border shadow-2xl">
          <div className="flex items-center border-b border-border px-4 py-4">
            <Search className="mr-3 h-5 w-5 shrink-0 text-muted-foreground opacity-50" />
            <input
              placeholder="Type a command or search..."
              className="flex h-10 w-full rounded-md bg-transparent text-lg outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50 font-bold uppercase italic tracking-tighter"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>
          <div className="max-h-[400px] overflow-y-auto p-2">
            {filteredItems.length === 0 && (
              <div className="py-14 text-center text-sm">
                <p className="text-muted-foreground uppercase font-black tracking-widest">No results found.</p>
              </div>
            )}
            {filteredItems.map((group) => (
              <div key={group.group} className="mb-4 last:mb-0">
                <div className="px-3 py-2 text-[10px] font-black uppercase tracking-[0.2em] text-primary/50">
                  {group.group}
                </div>
                <div className="space-y-1">
                  {group.items.map((item) => (
                    <button
                      key={item.label}
                      onClick={() => item.href ? (router.push(item.href), setOpen(false)) : item.action?.()}
                      className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm font-bold uppercase italic tracking-tight text-white hover:bg-primary/10 hover:text-primary transition-all group"
                    >
                      <item.icon className="h-5 w-5 text-muted-foreground group-hover:text-primary transition-colors" />
                      {item.label}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
          <div className="flex items-center justify-between border-t border-border px-4 py-3 bg-secondary/20">
            <div className="flex items-center gap-4 text-[10px] font-black uppercase tracking-widest text-muted-foreground">
              <span className="flex items-center gap-1"><kbd className="px-1 py-0.5 rounded border border-border bg-card">Enter</kbd> to select</span>
              <span className="flex items-center gap-1"><kbd className="px-1 py-0.5 rounded border border-border bg-card">↑↓</kbd> to navigate</span>
            </div>
            <div className="flex items-center gap-1 text-[10px] font-black uppercase tracking-widest text-primary/50">
              <Zap className="w-3 h-3 fill-current" />
              AI Powered
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
}
