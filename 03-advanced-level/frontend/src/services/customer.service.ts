import { NEXT_PUBLIC_API_URL } from "@/lib/constants";
import { supabase } from "@/lib/auth/supabase";

export interface Customer {
  id: number;
  name: string;
  email: string;
  industry: string;
  score: number;
  sentiment: string;
  last_activity: string;
  value: string;
}

export const customerService = {
  getCustomers: async (): Promise<Customer[]> => {
    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;
    
    const response = await fetch(`${NEXT_PUBLIC_API_URL}/api/v1/customers/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error("Failed to fetch customers");
    }
    return response.json();
  },
};
