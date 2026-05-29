"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/services/auth.service";
import { supabase } from "@/lib/auth/supabase";
import { Button } from "@/components/ui/button";
import { 
  LogOut, 
  UserCircle, 
  Menu, 
  X, 
  ExternalLink,
  Activity,
  MessageSquare,
  Zap,
  Book,
  Ticket,
  Users,
  Bot,
  Home
} from "lucide-react";
import { CommandPalette } from "@/components/shared/CommandPalette";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [userProfile, setUserProfile] = useState<{ name: string; avatar: string | null } | null>(null);

  useEffect(() => {
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser();
      if (user) {
        setUserProfile({
          name: user.user_metadata.full_name || user.email || 'User',
          avatar: user.user_metadata.avatar_url || null,
        });
      }
    };
    getUser();
  }, []);

  const handleLogout = async () => {
    await authService.signOut();
    router.push("/");
  };

  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden font-sans">
      {/* Mobile Sidebar Overlay */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/50 md:hidden"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`${
        isSidebarOpen ? "translate-x-0" : "-translate-x-full"
      } md:translate-x-0 fixed md:static z-50 w-72 h-full border-r border-border p-8 flex flex-col gap-10 bg-card/80 backdrop-blur-xl transition-transform duration-300`}>
        <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <Zap className="w-5 h-5 text-primary-foreground fill-current" />
              </div>
              <h2 className="text-2xl font-black text-white tracking-tighter uppercase italic">Ops<span className="text-primary">Core</span></h2>
            </div>
            <Button variant="ghost" className="md:hidden" onClick={() => setIsSidebarOpen(false)}>
                <X className="w-5 h-5" />
            </Button>
        </div>
        <nav className="space-y-8 flex-1">
          <div className="space-y-2">
            <h3 className="px-4 text-[10px] font-black text-primary uppercase tracking-[0.3em] mb-4 opacity-50">Platform Command</h3>
            {[
              { name: 'Home', href: '/', icon: Home },
              { name: 'Dashboard', href: '/dashboard', icon: Activity },
              { name: 'Neural Chat', href: '/dashboard/chat', icon: MessageSquare },
              { name: 'Workflows', href: '/dashboard/workflow', icon: Zap },
              { name: 'Knowledge', href: '/dashboard/knowledge', icon: Book },
              { name: 'Tickets', href: '/dashboard/tickets', icon: Ticket },
              { name: 'Intelligence', href: '/dashboard/crm', icon: Users },
              { name: 'Tracing', href: '/dashboard/logs', icon: Bot },
            ].map((item) => (
              <a 
                key={item.name}
                href={item.href}
                className="flex items-center gap-3 px-4 py-3 rounded-2xl transition-all text-sm font-bold uppercase italic tracking-tight text-muted-foreground hover:text-white hover:bg-secondary/50 group"
              >
                <item.icon className="w-4 h-4 group-hover:text-primary transition-colors" />
                {item.name}
              </a>
            ))}
          </div>
        </nav>
      </aside>
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col h-full overflow-hidden bg-[radial-gradient(circle_at_top_right,rgba(var(--primary),0.05),transparent_50%)]">
        <header className="h-20 border-b border-border flex items-center justify-between px-8 bg-card/50 backdrop-blur-md gap-4 z-30">
          <Button variant="ghost" className="md:hidden" onClick={() => setIsSidebarOpen(true)}>
            <Menu className="w-6 h-6" />
          </Button>
          
          <div className="flex-1 max-w-xl hidden md:block">
            <CommandPalette />
          </div>

          <div className="flex items-center gap-6">
            <div className="hidden md:flex flex-col items-end">
              <span className="text-xs font-black text-white uppercase italic tracking-tight">{userProfile?.name}</span>
              <span className="text-[10px] font-bold text-emerald-500 uppercase tracking-widest">Active Core</span>
            </div>
            <div className="w-10 h-10 rounded-2xl bg-secondary border border-border flex items-center justify-center overflow-hidden">
              {userProfile?.avatar ? (
                <img src={userProfile.avatar} alt="Profile" className="w-full h-full object-cover" />
              ) : (
                <UserCircle className="w-6 h-6 text-primary" />
              )}
            </div>
            <div className="h-8 w-px bg-border hidden md:block" />
            <Button variant="ghost" onClick={handleLogout} className="p-2 text-muted-foreground hover:text-destructive transition-colors">
              <LogOut className="w-5 h-5" />
            </Button>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
