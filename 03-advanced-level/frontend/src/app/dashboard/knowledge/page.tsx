"use client";
import { useState, useEffect } from "react";
import { 
  Library, 
  Search, 
  Plus, 
  FileText, 
  Book, 
  Settings, 
  Trash2, 
  ExternalLink,
  Loader2,
  CheckCircle2,
  AlertCircle
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardHeader, 
  CardTitle 
} from "@/components/ui/card";
import { knowledgeService, Knowledge } from "@/services/knowledge.service";

export default function KnowledgePage() {
  const [knowledge, setKnowledge] = useState<Knowledge[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    const fetchKnowledge = async () => {
      try {
        setIsLoading(true);
        const data = await knowledgeService.getKnowledge();
        setKnowledge(data);
        setError(null);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : "Failed to load knowledge base");
      } finally {
        setIsLoading(false);
      }
    };
    fetchKnowledge();
  }, []);

  const filteredKnowledge = knowledge.filter(item => 
    item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.category?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto p-4 md:p-8 space-y-8 animate-in fade-in duration-700">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div className="space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-bold uppercase tracking-widest">
            <Library className="w-3 h-3" />
            Neural Knowledge Base
          </div>
          <h1 className="text-4xl md:text-6xl font-black tracking-tighter text-white uppercase italic">
            Knowledge Hub
          </h1>
          <p className="text-muted-foreground max-w-2xl text-lg font-medium leading-relaxed">
            Upload and manage the documents your AI Agents use to resolve tickets and qualify leads. 
            Everything here is indexed for instant semantic retrieval.
          </p>
        </div>
        
        <Button className="px-8 py-6 rounded-2xl font-black uppercase tracking-widest italic shadow-xl shadow-primary/20">
          <Plus className="w-5 h-5 mr-2" />
          Add Document
        </Button>
      </div>

      <div className="flex gap-4 items-center bg-card border border-border p-2 rounded-2xl">
        <div className="relative flex-1">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <Input 
            placeholder="Search through your neural library..." 
            className="pl-11 border-none bg-transparent focus-visible:ring-0 text-base"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <div className="h-8 w-px bg-border mx-2" />
        <Button variant="ghost" size="icon">
          <Settings className="w-5 h-5" />
        </Button>
      </div>

      {isLoading ? (
        <div className="h-64 flex flex-col items-center justify-center gap-4">
          <Loader2 className="w-12 h-12 text-primary animate-spin" />
          <p className="text-xs font-black uppercase tracking-widest text-muted-foreground">Indexing Knowledge...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {knowledge.map((item) => (
            <Card key={item.id} className="bg-card/50 border-border hover:border-primary/50 transition-all group overflow-hidden rounded-[2rem]">
              <CardHeader className="relative">
                <div className="absolute top-6 right-6 p-2 rounded-xl bg-secondary/50 text-primary opacity-0 group-hover:opacity-100 transition-opacity">
                  <ExternalLink className="w-4 h-4" />
                </div>
                <div className="w-12 h-12 rounded-2xl bg-primary/10 border border-primary/20 flex items-center justify-center mb-2">
                  <FileText className="w-6 h-6 text-primary" />
                </div>
                <CardTitle className="text-xl font-black uppercase italic tracking-tight">{item.title}</CardTitle>
                <CardDescription className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded-full bg-secondary text-[8px] font-black uppercase tracking-widest text-muted-foreground">
                    {item.category}
                  </span>
                  <span className="text-[10px] text-muted-foreground font-medium">Used {item.last_used}</span>
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center gap-2 text-emerald-400">
                  <CheckCircle2 className="w-4 h-4" />
                  <span className="text-[10px] font-bold uppercase tracking-widest">Fully Indexed (RAG Ready)</span>
                </div>
                <div className="flex gap-2 pt-4">
                  <Button variant="secondary" className="flex-1 rounded-xl text-xs font-bold uppercase italic">View</Button>
                  <Button variant="ghost" size="icon" className="text-destructive hover:bg-destructive/10">
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* RAG Preview Section */}
      <div className="bg-primary/5 border border-primary/10 rounded-[2.5rem] p-8 md:p-12 flex flex-col md:flex-row gap-8 items-center">
        <div className="flex-1 space-y-4">
          <h2 className="text-2xl md:text-3xl font-black uppercase italic tracking-tighter">How RAG Works</h2>
          <p className="text-muted-foreground text-sm leading-relaxed">
            Retrieval-Augmented Generation (RAG) allows your agents to fetch relevant snippets from these documents before answering a customer. This ensures 100% accuracy and zero hallucinations.
          </p>
          <div className="flex gap-4 pt-4">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-primary" />
              <span className="text-[10px] font-black uppercase tracking-widest text-white">Embeddings</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-primary" />
              <span className="text-[10px] font-black uppercase tracking-widest text-white">Vector Search</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-primary" />
              <span className="text-[10px] font-black uppercase tracking-widest text-white">Context Injection</span>
            </div>
          </div>
        </div>
        <div className="w-full md:w-64 h-64 bg-card rounded-[2rem] border border-border p-6 flex items-center justify-center relative overflow-hidden">
           <Book className="w-24 h-24 text-primary opacity-20 animate-pulse" />
           <div className="absolute inset-0 bg-gradient-to-t from-primary/10 to-transparent" />
        </div>
      </div>
    </div>
  );
}
