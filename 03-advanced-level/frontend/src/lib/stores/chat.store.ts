import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  agent?: string;
  timestamp: string;
  sentiment?: string;
  sentimentScore?: number;
  thoughts?: string;
  channel?: 'web' | 'email' | 'whatsapp';
}

interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: string;
}

interface ChatState {
  conversations: Conversation[];
  activeConversationId: string | null;
  addMessage: (message: Message) => void;
  createNewConversation: () => void;
  setActiveConversation: (id: string) => void;
  deleteConversation: (id: string) => void;
  clearMessages: () => void;
}

export const useChatStore = create<ChatState>()(
  persist(
    (set, get) => ({
      conversations: [],
      activeConversationId: null,

      addMessage: (message) => set((state) => {
        const { conversations, activeConversationId } = state;
        
        const targetConversationId = activeConversationId;
        let updatedConversations = [...conversations];

        // If no active conversation, create one
        if (!targetConversationId) {
          const newId = Date.now().toString();
          const newConv: Conversation = {
            id: newId,
            title: message.content.slice(0, 30) + (message.content.length > 30 ? '...' : ''),
            messages: [message],
            createdAt: new Date().toISOString(),
          };
          return {
            conversations: [newConv, ...conversations],
            activeConversationId: newId
          };
        }

        // Update existing conversation
        updatedConversations = updatedConversations.map(conv => {
          if (conv.id === targetConversationId) {
            // Update title if it's the first user message
            let title = conv.title;
            if (conv.messages.length === 0 && message.role === 'user') {
              title = message.content.slice(0, 30) + (message.content.length > 30 ? '...' : '');
            }
            return { ...conv, messages: [...conv.messages, message], title };
          }
          return conv;
        });

        return { conversations: updatedConversations };
      }),

      createNewConversation: () => set((state) => ({
        activeConversationId: null
      })),

      setActiveConversation: (id) => set({ activeConversationId: id }),

      deleteConversation: (id) => set((state) => ({
        conversations: state.conversations.filter(c => c.id !== id),
        activeConversationId: state.activeConversationId === id ? null : state.activeConversationId
      })),

      clearMessages: () => set((state) => {
        if (!state.activeConversationId) return state;
        return {
          conversations: state.conversations.map(conv => 
            conv.id === state.activeConversationId ? { ...conv, messages: [] } : conv
          )
        };
      }),
    }),
    {
      name: 'chat-storage',
    }
  )
);
