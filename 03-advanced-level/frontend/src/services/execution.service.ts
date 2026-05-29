import { NEXT_PUBLIC_API_URL } from "@/lib/constants";
import { supabase } from "@/lib/auth/supabase";

export interface ExecutionLog {
  id: number;
  agent_name: string;
  action: string;
  status: string;
  details?: string;
  reasoning?: string;
  step_number: number;
  created_at: string;
}

export const executionService = {
  getLogs: async (): Promise<ExecutionLog[]> => {
    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;
    
    console.log("Debug - Session:", session);
    console.log("Debug - Token:", token);
    
    const response = await fetch(`${NEXT_PUBLIC_API_URL}/api/v1/logs/executions`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      console.error("Debug - Response Status:", response.status);
      throw new Error("Failed to fetch execution logs");
    }
    return response.json();
  },
};
