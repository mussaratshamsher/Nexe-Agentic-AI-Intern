import { NEXT_PUBLIC_API_URL } from "@/lib/constants";
import { supabase } from "@/lib/auth/supabase";

export interface Ticket {
  id: number;
  customer_id: number;
  priority: string;
  status: string;
  issue_summary: string;
  is_autopilot: number;
  ai_draft: string | null;
  created_at: string;
}

export interface CreateTicketDTO {
  customer_id: number;
  priority: string;
  issue_summary: string;
}

export interface UpdateTicketDTO {
  status?: string;
  priority?: string;
  ai_draft?: string | null;
}

export const ticketService = {
  getTickets: async (): Promise<Ticket[]> => {
    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;
    
    const response = await fetch(`${NEXT_PUBLIC_API_URL}/api/v1/tickets/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error("Failed to fetch tickets");
    }
    return response.json();
  },

  createTicket: async (ticketData: CreateTicketDTO): Promise<Ticket> => {
    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;
    
    const response = await fetch(`${NEXT_PUBLIC_API_URL}/api/v1/tickets/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(ticketData),
    });
    
    if (!response.ok) {
      throw new Error("Failed to create ticket");
    }
    return response.json();
  },

  updateTicket: async (id: number, updateData: UpdateTicketDTO): Promise<Ticket> => {
    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;
    
    const response = await fetch(`${NEXT_PUBLIC_API_URL}/api/v1/tickets/${id}`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updateData),
    });
    
    if (!response.ok) {
      throw new Error("Failed to update ticket");
    }
    return response.json();
  },
};
