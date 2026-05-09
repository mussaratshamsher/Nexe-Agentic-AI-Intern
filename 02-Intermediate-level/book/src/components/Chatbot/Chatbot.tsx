import React, { useState, useRef, useEffect } from 'react';
import styles from './Chatbot.module.css';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  sources?: string[];
}

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const initialMessage: Message = {
    id: 1,
    text: 'How can I help you today?',
    sender: 'bot',
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const [messages, setMessages] = useState<Message[]>([initialMessage]);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isOpen]);

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    const currentInputValue = inputValue;
    const userMessage: Message = {
      id: Date.now(),
      text: currentInputValue,
      sender: 'user'
    };

    setMessages(prev => [...prev, userMessage]); // Optimistically update UI
    setInputValue('');
    setIsLoading(true);

    try {
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      // API call to backend - use environment variable if available
      const API_URL = process.env.NODE_ENV === 'production' 
        ? 'https://ai-textbook-backend.railway.app/query' // Fallback to a placeholder or user's prod URL
        : 'http://localhost:8000/query';

      const response = await fetch(API_URL, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
          question: currentInputValue,
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const botMessage: Message = {
        id: Date.now() + 1,
        text: data.answer || 'Sorry, I couldn\'t process your request.',
        sender: 'bot',
        sources: data.sources,
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage: Message = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again later.',
        sender: 'bot'
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleIconKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      toggleChat();
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      {isOpen ? (
        <div className={`${styles.chatbotWindow} ${isOpen ? styles.open : ''}`}>
          <div className={styles.chatbotHeader}>
            <div className={styles.chatbotTitle}>Physical AI Assistant</div>
            <button
              className={styles.chatbotClose}
              onClick={toggleChat}
              aria-label="Close chat"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <div className={styles.chatMessages}>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`${styles.message} ${
                  message.sender === 'user' ? styles.userMessage : styles.botMessage
                }`}
              >
                <p dangerouslySetInnerHTML={{ __html: message.text.replace(/\n/g, '<br />') }} />
                {message.sources && message.sources.length > 0 && (
                  <div className={styles.sources}>
                    <strong>Sources:</strong>
                    <ul>
                      {message.sources.map((source, i) => (
                        <li key={i}>{source}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}

            {isLoading && (
              <div className={`${styles.message} ${styles.botMessage} ${styles.typingIndicator}`}>
                Thinking...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className={styles.chatInputArea}>
            <textarea
              className={styles.chatInput}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about Physical AI & Humanoid Robotics..."
              rows={1}
              disabled={isLoading}
            />
            <button
              className={styles.sendButton}
              onClick={handleSend}
              disabled={!inputValue.trim() || isLoading}
              aria-label="Send message"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="white">
                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
              </svg>
            </button>
          </div>
        </div>
      ) : (
        <div
          className={styles.chatbotIcon}
          onClick={toggleChat}
          onKeyDown={handleIconKeyDown}
          role="button"
          tabIndex={0}
          aria-label="Open chatbot"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 8V4H8" />
            <rect width="16" height="12" x="4" y="8" rx="2" />
            <path d="M2 14h2" />
            <path d="M20 14h2" />
            <path d="M15 13v2" />
            <path d="M9 13v2" />
          </svg>
        </div>
      )}
    </div>
  );
};

export default Chatbot;