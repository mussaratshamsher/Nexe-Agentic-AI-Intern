import { NEXT_PUBLIC_API_URL } from "@/lib/constants";
import { supabase } from "@/lib/auth/supabase";

export interface Knowledge {
  id: number;
  title: string;
  content: string;
  category: string;
  last_used?: string;
  created_at: string;
}

export interface KnowledgeData {
  title: string;
  content: string;
  category: string;
}

export const knowledgeService = {
  getKnowledge: async (): Promise<Knowledge[]> => {
    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;
    
    const response = await fetch(`${NEXT_PUBLIC_API_URL}/api/v1/knowledge/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error("Failed to fetch knowledge base");
    }
    return response.json();
  },

  addKnowledge: async (knowledgeData: KnowledgeData): Promise<Knowledge> => {
    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;
    
    const response = await fetch(`${NEXT_PUBLIC_API_URL}/api/v1/knowledge/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(knowledgeData),
    });
    
    if (!response.ok) {
      throw new Error("Failed to add knowledge");
    }
    return response.json();
  },
};
