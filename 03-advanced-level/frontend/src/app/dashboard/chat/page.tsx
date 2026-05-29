"use client";

import { useState, useRef, useEffect, useMemo } from "react";
import { useChatStore } from "@/lib/stores/chat.store";
import { Button, buttonVariants } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import { 
  Bot, 
  User, 
  AlertCircle, 
  SendHorizontal, 
  Plus, 
  MessageSquare, 
  Trash2,
  ChevronLeft,
  Loader2,
  MoreVertical,
  History,
  Settings2,
  MoreHorizontal,
  Menu,
  X,
  Copy,
  Check,
  Download,
  Mail,
  Globe,
  MessageCircle
} from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
  DropdownMenuLabel,
  DropdownMenuGroup,
} from "@/components/ui/dropdown-menu";
import { supabase } from "@/lib/auth/supabase";

export default function ChatPage() {
  const { 
    conversations, 
    activeConversationId, 
    addMessage, 
    createNewConversation, 
    setActiveConversation,
    deleteConversation,
    clearMessages
  } = useChatStore();

  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(() => typeof window !== 'undefined' && window.innerWidth >= 768); 
  const [userProfile, setUserProfile] = useState<{ name: string } | null>(null);

  useEffect(() => {
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser();
      if (user) {
        setUserProfile({
          name: user.user_metadata.full_name || user.email?.split('@')[0] || 'User',
        });
      }
    };
    getUser();
  }, []);

  const scrollRef = useRef<HTMLDivElement>(null);

  const activeConversation = conversations.find(c => c.id === activeConversationId);
  const messages = activeConversation?.messages || [];

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const downloadFullChatPDF = async () => {
    const element = scrollRef.current;
    if (!element) return;

    const canvas = await html2canvas(element);
    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF();
    const imgProps = pdf.getImageProperties(imgData);
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

    pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
    pdf.save(`chat-conversation-${activeConversationId || 'new'}.pdf`);
  };

  const [channel, setChannel] = useState<"web" | "email" | "whatsapp">("web");

  const generateId = () => Date.now().toString();

  const handleSend = async () => {
    if (!input.trim()) return;
    
    setError(null);
    const userMsg = input;
    setInput("");
    
    addMessage({
      id: generateId(),
      role: 'user',
      content: userMsg,
      timestamp: new Date().toISOString(),
      channel: channel
    });
    
    setIsLoading(true);

    try {
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;
      
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/chat/message`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          customer_id: 1, 
          message: userMsg,
          channel: channel
        })
      });

      if (!response.ok) {
        throw new Error(response.status === 401 ? "Unauthorized. Please login again." : "Failed to connect to AI server.");
      }

      const reader = response.body?.getReader();
      if (!reader) throw new Error("Stream reader not available");

      const assistantMsgId = (parseInt(generateId()) + 1).toString();
      let fullContent = "";
      let metadataReceived = false;

      addMessage({
        id: assistantMsgId,
        role: 'assistant',
        content: "",
        timestamp: new Date().toISOString(),
        channel: channel
      });

      const decoder = new TextDecoder();
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        
        if (!metadataReceived && chunk.includes("|||")) {
          const parts = chunk.split("|||");
          try {
            const metadata = JSON.parse(parts[0]);
            useChatStore.setState((state) => ({
              conversations: state.conversations.map(c => 
                c.id === activeConversationId 
                  ? { 
                      ...c, 
                      messages: c.messages.map(m => 
                        m.id === assistantMsgId ? { ...m, thoughts: metadata.strategic_reasoning } : m
                      ) 
                    } 
                  : c
              )
            }));
            
            if (parts[1]) {
                fullContent += parts[1];
                updateStreamingMessage(assistantMsgId, fullContent);
            }
          } catch (e) {
            console.error("Metadata parse error", e);
          }
          metadataReceived = true;
        } else {
          fullContent += chunk;
          updateStreamingMessage(assistantMsgId, fullContent);
        }
      }

    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const updateStreamingMessage = (id: string, content: string) => {
    useChatStore.setState((state) => ({
      conversations: state.conversations.map(c => 
        c.id === activeConversationId 
          ? { 
              ...c, 
              messages: c.messages.map(m => 
                m.id === id ? { ...m, content } : m
              ) 
            } 
          : c
      )
    }));
  };

  const CopyButton = ({ content }: { content: string }) => {
    const [copied, setCopied] = useState(false);
    return (
      <button
        onClick={(e) => {
          e.stopPropagation();
          navigator.clipboard.writeText(content);
          setCopied(true);
          setTimeout(() => setCopied(false), 2000);
        }}
        className="p-1.5 rounded-lg bg-secondary/50 border border-border hover:border-primary/50 hover:bg-primary/10 transition-all group/copy"
        title="Copy to clipboard"
      >
        {copied ? (
          <Check className="w-3.5 h-3.5 text-emerald-500" />
        ) : (
          <Copy className="w-3.5 h-3.5 text-muted-foreground group-hover/copy:text-primary" />
        )}
      </button>
    );
  };

  const MessageActions = ({ content, id }: { content: string, id: string }) => {
    const downloadMessagePDF = () => {
      const pdf = new jsPDF();
      const margin = 20;
      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();
      let cursorY = 20;

      // Header
      pdf.setFont("helvetica", "bold");
      pdf.setFontSize(18);
      pdf.setTextColor("#facc15"); // Hardcoded primary brand color for PDF stability
      pdf.text("NEURAL TRACE EXPORT", margin, cursorY);
      cursorY += 12;
      
      // Metadata
      pdf.setFont("helvetica", "normal");
      pdf.setFontSize(9);
      pdf.setTextColor(150);
      pdf.text(`ORCHESTRATION ID: ${id.toUpperCase()}`, margin, cursorY);
      cursorY += 5;
      pdf.text(`TIMESTAMP: ${new Date().toLocaleString().toUpperCase()}`, margin, cursorY);
      cursorY += 5;
      pdf.text(`PROTOCOL: SECURE BUSINESS INTELLIGENCE`, margin, cursorY);
      cursorY += 8;
      
      // Divider
      pdf.setDrawColor(230);
      pdf.setLineWidth(0.5);
      pdf.line(margin, cursorY, pageWidth - margin, cursorY);
      cursorY += 15;
      
      // Content
      pdf.setTextColor(40);
      pdf.setFontSize(11);
      pdf.setFont("helvetica", "normal");
      
      const splitText = pdf.splitTextToSize(content, pageWidth - (margin * 2));
      const lineHeight = 7;

      for (let i = 0; i < splitText.length; i++) {
        // Check if we need a new page
        if (cursorY > pageHeight - margin) {
          pdf.addPage();
          cursorY = 20;
          // Add a small header on new pages
          pdf.setFontSize(8);
          pdf.setTextColor(200);
          pdf.text(`TRACING CONTINUED - ID: ${id.slice(0, 8)}`, margin, cursorY - 5);
          pdf.setFontSize(11);
          pdf.setTextColor(40);
        }
        pdf.text(splitText[i], margin, cursorY);
        cursorY += lineHeight;
      }

      // Footer
      if (cursorY > pageHeight - 30) {
        pdf.addPage();
        cursorY = 20;
      }
      cursorY += 10;
      pdf.setDrawColor(240);
      pdf.line(margin, cursorY, pageWidth - margin, cursorY);
      cursorY += 10;
      pdf.setFontSize(8);
      pdf.setTextColor(180);
      pdf.setFont("helvetica", "italic");
      pdf.text("This document was generated autonomously by OpsCore Multi-Agent Systems.", margin, cursorY);
      
      pdf.save(`neural-trace-${id.slice(-6)}.pdf`);
    };

    const varToRgb = (varName: string) => {
      if (typeof window === 'undefined') return null;
      const val = getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
      if (val.includes(' ')) {
        const parts = val.split(' ');
        return `rgb(${parts.join(',')})`;
      }
      return val;
    };

    return (
      <div className="flex items-center gap-2 mt-4 pt-3 border-t border-border/10">
        <CopyButton content={content} />
        <button
          onClick={(e) => {
            e.stopPropagation();
            downloadMessagePDF();
          }}
          className="p-1.5 rounded-lg bg-secondary/50 border border-border hover:border-primary/50 hover:bg-primary/10 transition-all group/pdf"
          title="Download as PDF"
        >
          <Download className="w-3.5 h-3.5 text-muted-foreground group-hover/pdf:text-primary" />
        </button>
        <div className="h-4 w-px bg-border/20 mx-1" />
        <div className="text-[8px] font-black uppercase tracking-[0.2em] text-muted-foreground/50">
          Secure Export
        </div>
      </div>
    );
  };

  return (
    <div className="flex h-[calc(100vh-2rem)] md:h-[calc(100vh-4rem)] w-full border-none md:border md:border-border md:rounded-2xl bg-card overflow-hidden relative">
      
      {/* Mobile Sidebar Overlay */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm md:hidden"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Sidebar - History Drawer */}
      <aside className={`
        fixed md:static inset-y-0 left-0 z-50 
        ${isSidebarOpen ? 'translate-x-0 w-72 md:w-80' : '-translate-x-full w-0 md:w-0'} 
        transition-all duration-300 ease-in-out
        border-r border-border bg-secondary/30 md:bg-secondary/20 flex flex-col overflow-hidden
      `}>
        <div className="p-4 border-b border-border flex items-center justify-between shrink-0 bg-background/50">
          <div className="flex items-center gap-2">
            <History className="w-5 h-5 text-primary" />
            <h3 className="font-bold text-sm uppercase tracking-widest text-foreground">Chat History</h3>
          </div>
          <Button variant="ghost" size="icon" className="h-8 w-8 md:hidden" onClick={() => setIsSidebarOpen(false)}>
            <X className="w-5 h-5" />
          </Button>
          <Button variant="ghost" size="icon" className="h-8 w-8 hidden md:flex" onClick={createNewConversation} title="New Chat">
            <Plus className="w-4 h-4" />
          </Button>
        </div>
        
        <ScrollArea className="flex-1 bg-transparent">
          <div className="p-3 space-y-1">
            <Button 
              variant="outline" 
              className="w-full justify-start gap-2 mb-4 md:hidden border-dashed hover:border-primary text-xs"
              onClick={() => {
                createNewConversation();
                setIsSidebarOpen(false);
              }}
            >
              <Plus className="w-4 h-4" />
              New Conversation
            </Button>

            {conversations.length === 0 ? (
              <div className="text-center py-12 px-4">
                <p className="text-xs text-muted-foreground italic">Your history will appear here</p>
              </div>
            ) : (
              conversations.map((conv) => (
                <div 
                  key={conv.id}
                  className={`group flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-all duration-200 ${
                    activeConversationId === conv.id 
                      ? 'bg-primary/15 text-primary shadow-sm border border-primary/10' 
                      : 'hover:bg-secondary/80 border border-transparent'
                  }`}
                  onClick={() => {
                    setActiveConversation(conv.id);
                    if (window.innerWidth < 768) setIsSidebarOpen(false);
                  }}
                >
                  <MessageSquare className={`w-4 h-4 shrink-0 ${activeConversationId === conv.id ? 'opacity-100' : 'opacity-40'}`} />
                  <span className="text-xs font-semibold truncate flex-1">{conv.title}</span>
                  
                  <DropdownMenu>
                    <DropdownMenuTrigger 
                      className={cn(
                        buttonVariants({ variant: "ghost", size: "icon" }),
                        "w-8 h-8 opacity-0 group-hover:opacity-100 focus:opacity-100 transition-opacity"
                      )}
                      onClick={(e) => e.stopPropagation()}
                    >
                      <MoreVertical className="w-4 h-4" />
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end" className="w-44 p-1">
                      <DropdownMenuGroup>
                        <DropdownMenuLabel className="text-[10px] px-2 py-1.5 uppercase text-muted-foreground font-bold">Manage Chat</DropdownMenuLabel>
                        <DropdownMenuItem 
                          className="text-destructive focus:bg-destructive/10 focus:text-destructive gap-3 cursor-pointer rounded-lg py-2"
                          onClick={(e) => {
                            e.stopPropagation();
                            deleteConversation(conv.id);
                          }}
                        >
                          <Trash2 className="w-4 h-4" />
                          <span className="font-medium">Delete Forever</span>
                        </DropdownMenuItem>
                      </DropdownMenuGroup>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              ))
            )}
          </div>
        </ScrollArea>

        {/* Sidebar Footer */}
        <div className="p-4 border-t border-border bg-secondary/20">
          <DropdownMenu>
            <DropdownMenuTrigger 
              className={cn(
                buttonVariants({ variant: "outline" }),
                "w-full justify-start gap-3 h-11 px-4 border shadow-sm hover:border-primary/50 transition-all text-sm font-medium"
              )}
            >
              <Settings2 className="w-4 h-4 text-primary" />
              <span>Control Center</span>
              <MoreHorizontal className="w-4 h-4 ml-auto opacity-40" />
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-64 p-2" align="start" side="top" sideOffset={10}>
              <DropdownMenuGroup>
                <DropdownMenuLabel className="px-2 py-1.5 text-xs font-bold uppercase text-muted-foreground">General Actions</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem className="gap-3 cursor-pointer rounded-lg py-2.5" onClick={createNewConversation}>
                  <Plus className="w-4 h-4" />
                  <span className="font-medium">Start New Chat</span>
                </DropdownMenuItem>
                <DropdownMenuItem 
                  className="text-destructive focus:bg-destructive/10 focus:text-destructive gap-3 cursor-pointer rounded-lg py-2.5"
                  onClick={() => {
                    if (confirm("This will clear all messages in this conversation. Continue?")) clearMessages();
                  }}
                  disabled={!activeConversationId}
                >
                  <Trash2 className="w-4 h-4" />
                  <span className="font-medium">Clear All Messages</span>
                </DropdownMenuItem>
              </DropdownMenuGroup>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </aside>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-w-0 relative bg-background">
        
        {/* Chat Header */}
        <header className="h-16 border-b border-border flex items-center justify-between px-4 md:px-6 shrink-0 bg-card/80 backdrop-blur-md sticky top-0 z-30 shadow-sm">
          <div className="flex items-center gap-3">
            <Button 
              variant="ghost" 
              size="icon" 
              className="h-10 w-10 hover:bg-secondary"
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            >
              {isSidebarOpen && window.innerWidth >= 768 ? <ChevronLeft className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </Button>
            <div className="hidden md:block">
              <h2 className="text-base font-bold tracking-tight">AI Assistant</h2>
              <div className="flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.6)] animate-pulse" />
                <p className="text-[10px] text-muted-foreground uppercase tracking-widest font-bold">Secure Connection</p>
              </div>
            </div>
          </div>

          <div className="md:absolute md:left-1/2 md:-translate-x-1/2 text-center">
            <h1 className="text-sm md:text-lg font-black tracking-tighter uppercase italic text-primary">Personal Manager </h1>
            <p className="text-[8px] md:text-[10px] text-muted-foreground font-mono uppercase tracking-[0.2em] hidden md:block">Multi-Agent Intelligence</p>
          </div>

          <div className="flex items-center gap-2">
            <Button 
                variant="ghost" 
                size="icon" 
                className="h-10 w-10 hover:bg-secondary"
                onClick={downloadFullChatPDF}
                title="Download Conversation as PDF"
            >
                <Download className="w-5 h-5" />
            </Button>
            <Button 
              variant="ghost" 
              size="icon" 
              className="h-10 w-10 md:hidden"
              onClick={createNewConversation}
            >
              <Plus className="w-5 h-5" />
            </Button>
            <DropdownMenu>
              <DropdownMenuTrigger 
                className={cn(
                  buttonVariants({ variant: "ghost", size: "icon" }),
                  "h-10 w-10 hover:bg-secondary"
                )}
              >
                <MoreHorizontal className="w-6 h-6" />
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56 p-2">
                <DropdownMenuGroup>
                  <DropdownMenuLabel className="px-2 py-1.5 text-xs font-bold uppercase text-muted-foreground">Chat Options</DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem className="gap-3 cursor-pointer rounded-lg py-2.5" onClick={() => setIsSidebarOpen(!isSidebarOpen)}>
                    <History className="w-4 h-4" />
                    <span className="font-medium">View History</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem 
                    className="text-destructive focus:bg-destructive/10 focus:text-destructive gap-3 cursor-pointer rounded-lg py-2.5"
                    onClick={() => {
                      if (activeConversationId) deleteConversation(activeConversationId);
                    }}
                    disabled={!activeConversationId}
                  >
                    <Trash2 className="w-4 h-4" />
                    <span className="font-medium">Delete This Chat</span>
                  </DropdownMenuItem>
                </DropdownMenuGroup>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </header>

        {/* Messages Scroll Area */}
        <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-6 md:p-12 space-y-8 bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-primary/5 via-transparent to-transparent">
          {messages.length === 0 && !isLoading && (
            <div className="h-full flex flex-col items-center justify-center text-muted-foreground space-y-8 max-w-lg mx-auto">
              <div className="relative">
                <div className="w-24 h-24 rounded-[2.5rem] bg-gradient-to-br from-primary/20 to-primary/5 border border-primary/20 flex items-center justify-center shadow-xl animate-float">
                  <Bot className="w-12 h-12 text-primary" />
                </div>
                <div className="absolute -bottom-2 -right-2 w-10 h-10 rounded-full bg-background border border-border flex items-center justify-center shadow-lg">
                  <Plus className="w-5 h-5 text-primary" />
                </div>
              </div>
              <div className="text-center space-y-3">
                <h3 className="font-black text-sm md:text-lg lg:text-xl text-foreground tracking-tight uppercase italic">Autonomous Operations</h3>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
                {[
                  { label: 'Sales Lead', desc: 'Create a new qualification', icon: '💰' },
                  { label: 'Content Plan', desc: 'Generate marketing ideas', icon: '✍️' },
                  { label: 'Ticket Status', desc: 'Check support queue', icon: '🎫' },
                  { label: 'Project Plan', desc: 'Draft a new timeline', icon: '📅' }
                ].map((s) => (
                  <button 
                    key={s.label}
                    className="p-4 text-left border border-border rounded-2xl hover:bg-card hover:border-primary/40 hover:shadow-lg transition-all group relative overflow-hidden bg-card/40"
                    onClick={() => setInput(`I want to ${s.label.toLowerCase()}`)}
                  >
                    <div className="flex items-center gap-3 mb-1">
                      <span className="text-xl">{s.icon}</span>
                      <span className="font-bold text-xs uppercase tracking-wider group-hover:text-primary transition-colors">{s.label}</span>
                    </div>
                    <span className="text-[10px] text-muted-foreground font-medium">{s.desc}</span>
                    <div className="absolute top-0 right-0 w-1 h-full bg-primary transform scale-y-0 group-hover:scale-y-100 transition-transform origin-top" />
                  </button>
                ))}
              </div>
            </div>
          )}
          
          {messages.map((m) => (
            <div 
              key={m.id} 
              className={`flex flex-col gap-4 ${m.role === 'user' ? 'items-end' : 'items-start'} group`}
            >
              {m.role === 'assistant' && m.thoughts && (
                <div className="flex gap-3 items-center ml-14 animate-in slide-in-from-left duration-500">
                  <div className="w-2 h-2 rounded-full bg-primary animate-ping" />
                  <div className="px-4 py-2 rounded-2xl bg-primary/5 border border-primary/10 text-[10px] font-bold uppercase tracking-wider text-primary italic">
                    Thinking: {m.thoughts}
                  </div>
                </div>
              )}

              <div className={`flex gap-3 md:gap-6 ${m.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                {m.role !== 'user' ? (
                  <div className="w-10 h-10 rounded-2xl bg-primary text-primary-foreground flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-primary/20 border border-primary/50">
                    <Bot className="w-6 h-6" />
                  </div>
                ) : (
                  <div className="w-10 h-10 rounded-2xl bg-secondary border-2 border-border flex items-center justify-center shrink-0 mt-1 shadow-sm">
                    <User className="w-6 h-6 text-primary" />
                  </div>
                )}
                
                <div className={`
                  relative max-w-[88%] md:max-w-[75%] px-5 py-4 md:px-7 md:py-6 rounded-[2.5rem] text-sm md:text-base leading-relaxed shadow-sm transition-all
                  ${m.role === 'user' 
                    ? 'bg-primary text-primary-foreground rounded-tr-none font-medium' 
                    : m.channel === 'email' 
                      ? 'bg-card border-2 border-primary/20 rounded-tl-none font-serif shadow-xl' 
                      : m.channel === 'whatsapp'
                        ? 'bg-emerald-500/10 border-l-4 border-emerald-500 rounded-tl-none font-medium text-foreground/90'
                        : 'bg-card border border-border rounded-tl-none font-medium text-foreground/90'}
                `}>
                  {m.role === 'assistant' && (                 
                    <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity z-50 pointer-events-auto">
                      <CopyButton content={m.content} />
                    </div>
                  )}

                  {m.channel && m.role === 'assistant' && (
                    <div className={`mb-3 inline-flex items-center gap-2 px-2 py-0.5 rounded-full border text-[8px] font-black uppercase tracking-widest ${
                      m.channel === 'email' ? 'bg-blue-500/10 border-blue-500/20 text-blue-500' :
                      m.channel === 'whatsapp' ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-500' :
                      'bg-primary/10 border-primary/20 text-primary'
                    }`}>
                      {m.channel === 'email' ? <Mail className="w-2.5 h-2.5" /> :
                       m.channel === 'whatsapp' ? <MessageCircle className="w-2.5 h-2.5" /> :
                       <Globe className="w-2.5 h-2.5" />}
                      {m.channel} Protocol
                    </div>
                  )}
                  
                  {m.role === 'user' && m.sentiment && (
                    <div className="absolute -top-3 right-4 px-2 py-0.5 rounded-full bg-secondary border border-border text-[8px] font-black uppercase tracking-tighter text-primary shadow-sm">
                      Sentiment: {m.sentiment}
                    </div>
                  )}

                  <div className={`${m.channel === 'email' ? 'text-sm' : ''} whitespace-pre-wrap`}>
                    {m.channel === 'email' && m.role === 'assistant' && (
                      <div className="mb-4 pb-4 border-b border-primary/10 space-y-1">
                        <p className="text-[10px] font-black uppercase text-muted-foreground tracking-widest">Subject: RE: {userProfile?.name || 'User'}&apos;s Inquiry</p>
                        <p className="text-[10px] font-black uppercase text-muted-foreground tracking-widest">From: Managing Chief</p>
                      </div>
                    )}
                    {m.content}
                    {m.channel === 'email' && m.role === 'assistant' && (
                      <div className="mt-8 pt-4 border-t border-primary/10 italic text-[10px] text-muted-foreground">
                        Best regards,<br/>
                        Managing Chief
                      </div>
                    )}
                  </div>
                  
                  <MessageActions content={m.content} id={m.id} />

                  <div className={`text-[9px] mt-4 opacity-40 font-black tracking-widest uppercase flex items-center gap-2 ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <span>{new Date(m.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                    <span className="w-1 h-1 rounded-full bg-current" />
                    <span>{m.role === 'user' ? 'Sent' : 'Agent Response'}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex gap-4 md:gap-6 justify-start">
              <div className="w-10 h-10 rounded-2xl bg-primary flex items-center justify-center shrink-0 shadow-lg shadow-primary/20">
                <Loader2 className="w-6 h-6 text-primary-foreground animate-spin" />
              </div>
              <div className="bg-card border border-border text-muted-foreground px-6 py-4 rounded-[2rem] rounded-tl-none shadow-sm flex items-center gap-4">
                <div className="flex gap-1.5">
                  <span className="w-2 h-2 bg-primary/40 rounded-full animate-bounce [animation-delay:-0.3s]" />
                  <span className="w-2 h-2 bg-primary/40 rounded-full animate-bounce [animation-delay:-0.15s]" />
                  <span className="w-2 h-2 bg-primary/40 rounded-full animate-bounce" />
                </div>
                <span className="text-xs md:text-sm font-bold uppercase tracking-tighter italic">Orchestrating specialized agents...</span>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <footer className="p-4 md:p-8 bg-background/80 backdrop-blur-xl shrink-0 z-20">
          <div className="max-w-4xl mx-auto space-y-4">
            {error && (
              <div className="p-4 bg-destructive/5 text-destructive text-xs border border-destructive/20 rounded-2xl flex items-center gap-3 animate-shake">
                <AlertCircle className="w-5 h-5 shrink-0" />
                <span className="font-bold uppercase tracking-tight">{error}</span>
              </div>
            )}
            
            <div className="flex items-center gap-4 justify-center pb-2">
              {[
                { id: 'web', icon: Globe, label: 'Web Chat' },
                { id: 'email', icon: Mail, label: 'Email Bot' },
                { id: 'whatsapp', icon: MessageCircle, label: 'WhatsApp' }
              ].map((c) => (
                <button
                  key={c.id}
                  onClick={() => setChannel(c.id as "web" | "email" | "whatsapp")}
                  className={`flex items-center gap-2 px-4 py-2 rounded-xl border transition-all ${
                    channel === c.id 
                      ? 'bg-primary/10 border-primary text-primary shadow-lg shadow-primary/10' 
                      : 'border-border text-muted-foreground hover:border-primary/50'
                  }`}
                >
                  <c.icon className="w-4 h-4" />
                  <span className="text-[10px] font-black uppercase tracking-widest">{c.label}</span>
                </button>
              ))}
            </div>
            
            <div className="relative flex items-end gap-3 bg-card border border-border p-2 rounded-[2.5rem] shadow-2xl focus-within:border-primary/50 transition-all">
              <div className="relative flex-1 group pl-4">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Tell me what you need..."
                  rows={1}
                  className="w-full bg-transparent border-none px-2 py-3 focus:outline-none focus:ring-0 resize-none min-h-[40px] max-h-30 text-sm md:text-base font-medium placeholder:text-muted-foreground/50 transition-all"
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
                      e.preventDefault();
                      handleSend();
                    }
                  }}
                  disabled={isLoading}
                  style={{ height: 'auto' }}
                  onInput={(e) => {
                    const target = e.target as HTMLTextAreaElement;
                    target.style.height = 'auto';
                    target.style.height = `${target.scrollHeight}px`;
                  }}
                />
              </div>
              <Button 
                onClick={handleSend} 
                disabled={isLoading || !input.trim()} 
                size="icon"
                className={`
                  h-12 w-12 md:h-14 md:w-14 rounded-[2rem] shrink-0 transition-all duration-300 shadow-xl
                  ${input.trim() ? 'bg-primary scale-100 shadow-primary/30' : 'bg-muted scale-95 opacity-50'}
                `}
              >
                {isLoading ? <Loader2 className="w-5 h-5 md:w-6 md:h-6 animate-spin" /> : <SendHorizontal className="w-5 h-5 md:w-6 md:h-6" />}
              </Button>
            </div>
            
          </div>
        </footer>
      </div>
    </div>
  );
}
