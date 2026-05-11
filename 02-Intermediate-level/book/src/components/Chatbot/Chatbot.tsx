import React, { useState, useRef, useEffect, useContext } from 'react';
import styles from './Chatbot.module.css';
import { useAuth } from '../../auth/AuthContext';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  sources?: string[];
  tool_used?: string;
}

const Chatbot = () => {
  const { user } = useAuth();
  const { siteConfig } = useDocusaurusContext();
  const BACKEND_URL = (siteConfig.customFields?.backendUrl as string) || 'http://localhost:8000';
  
  const [isOpen, setIsOpen] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');
  const [showFiles, setShowFiles] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<any[]>([]);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const initialMessage: Message = {
    id: 1,
    text: 'Hi! I am your Physical AI Agent. I can search the book, the web, save notes, or email you info. How can I help?',
    sender: 'bot',
  };

  const [messages, setMessages] = useState<Message[]>([initialMessage]);

  // Load messages from localStorage on mount or when user changes
  useEffect(() => {
    if (user?.email) {
      const savedMessages = localStorage.getItem(`chat_history_${user.email}`);
      if (savedMessages) {
        try {
          setMessages(JSON.parse(savedMessages));
        } catch (e) {
          console.error('Error parsing saved messages:', e);
          setMessages([initialMessage]);
        }
      } else {
        setMessages([initialMessage]);
      }
    } else {
      setMessages([initialMessage]);
    }
  }, [user]);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    if (user?.email && messages.length > 0) {
      localStorage.setItem(`chat_history_${user.email}`, JSON.stringify(messages));
    }
  }, [messages, user]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isOpen]);

  const fetchFiles = async () => {
    if (!user) {
      console.log('No user logged in, skipping fetchFiles');
      return;
    }
    try {
      console.log(`Fetching files for user: ${user.email}`);
      const response = await fetch(`${BACKEND_URL}/files?user_email=${user.email}`);
      const data = await response.json();
      if (data.error) {
        console.error('Backend error fetching files:', data.error);
        setUploadStatus(`Error: ${data.error}`);
        setTimeout(() => setUploadStatus(''), 5000);
      }
      setUploadedFiles(data.files || []);
    } catch (error) {
      console.error('Network error fetching files:', error);
      setUploadStatus('Network error fetching files');
      setTimeout(() => setUploadStatus(''), 5000);
    }
  };

  useEffect(() => {
    if (showFiles) {
      fetchFiles();
    }
  }, [showFiles]);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !user) return;

    setUploadStatus('Uploading...');
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_email', user.email);

    try {
      const response = await fetch(`${BACKEND_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setUploadStatus('✅ Uploaded!');
        fetchFiles();
        setTimeout(() => setUploadStatus(''), 3000);
      } else {
        setUploadStatus('❌ Failed');
      }
    } catch (error) {
      setUploadStatus('❌ Error');
    }
  };

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading || !user) return;

    const currentInputValue = inputValue;
    const userMessage: Message = {
      id: Date.now(),
      text: currentInputValue,
      sender: 'user'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const API_URL = `${BACKEND_URL}/query`;

      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: currentInputValue,
          user_email: user.email
        })
      });

      const data = await response.json();

      const botMessage: Message = {
        id: Date.now() + 1,
        text: data.answer,
        sender: 'bot',
        sources: data.sources,
        tool_used: data.tool_used
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Is the backend running?',
        sender: 'bot'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const [emailingMessageId, setEmailingMessageId] = useState<number | null>(null);
  const [targetEmail, setTargetEmail] = useState('');

  const handleSendEmail = async (content: string) => {
    if (!targetEmail || !user) return;

    try {
      const response = await fetch(`${BACKEND_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: `Email this content to ${targetEmail}: ${content}`,
          user_email: user.email
        })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setEmailingMessageId(null);
        setTargetEmail('');
        alert(data.answer || 'Email process completed!');
      } else {
        alert('Error: ' + (data.detail || 'Failed to send email request'));
      }
    } catch (error) {
      console.error('Error sending email:', error);
      alert('Network error while sending email.');
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      {isOpen ? (
        <div className={`${styles.chatbotWindow} ${styles.open}`}>
          <div className={styles.chatbotHeader}>
            <div className={styles.chatbotTitle}>
               {showFiles ? 'My Uploaded Files' : 'Physical AI Agent'}
            </div>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button 
                className={styles.chatbotClose} 
                onClick={() => setShowFiles(!showFiles)}
                title={showFiles ? "Back to Chat" : "View Files"}
              >
                {showFiles ? '💬' : '📁'}
              </button>
              <button className={styles.chatbotClose} onClick={() => setIsOpen(false)}>✕</button>
            </div>
          </div>

          {showFiles ? (
            <div className={styles.chatMessages}>
              {uploadedFiles.length === 0 ? (
                <div className={styles.botMessage} style={{ padding: '20px', textAlign: 'center' }}>
                  No files uploaded yet.
                </div>
              ) : (
                <div className={styles.fileList}>
                  {uploadedFiles.map((file, idx) => (
                    <div key={idx} className={styles.fileItem}>
                      <span className={styles.fileName}>{file.filename}</span>
                      <span className={styles.fileDate}>{new Date(file.timestamp).toLocaleDateString()}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div className={styles.chatMessages}>
              {messages.map((message) => (
                <div key={message.id} className={`${styles.message} ${message.sender === 'user' ? styles.userMessage : styles.botMessage}`}>
                  <p dangerouslySetInnerHTML={{ __html: message.text.replace(/\n/g, '<br />') }} />
                  {message.tool_used && (
                    <span className={styles.toolBadge}>Tool: {message.tool_used}</span>
                  )}
                  
                  {message.sender === 'bot' && message.id !== 1 && (
                    <div className={styles.messageActions}>
                      <button 
                        className={styles.actionButton} 
                        onClick={() => {
                          setEmailingMessageId(emailingMessageId === message.id ? null : message.id);
                          setTargetEmail(user?.email || '');
                        }}
                        title="Email this content"
                      >
                        📧
                      </button>
                    </div>
                  )}

                  {emailingMessageId === message.id && (
                    <div className={styles.emailForm}>
                      <input 
                        type="email" 
                        placeholder="Recipient email"
                        value={targetEmail}
                        onChange={(e) => setTargetEmail(e.target.value)}
                        className={styles.emailInput}
                      />
                      <button 
                        onClick={() => handleSendEmail(message.text)}
                        className={styles.emailSendButton}
                      >
                        Send
                      </button>
                    </div>
                  )}
                </div>
              ))}
              {isLoading && <div className={styles.typingIndicator}>Thinking...</div>}
              <div ref={messagesEndRef} />
            </div>
          )}

          <div className={styles.chatInputArea}>
            {!user ? (
              <div className={styles.loginRequired}>
                <p>Please log in to use the AI Agent</p>
                <a href="/login" className={styles.loginLink}>Login Here</a>
              </div>
            ) : (
              <>
                <input
                  type="file"
                  ref={fileInputRef}
                  style={{ display: 'none' }}
                  onChange={handleFileUpload}
                  accept=".txt,.md,.pdf"
                />
                <button 
                  className={styles.uploadButton} 
                  onClick={() => fileInputRef.current?.click()}
                  title="Upload Knowledge"
                  disabled={showFiles}
                >
                  📎
                </button>
                <textarea
                  className={styles.chatInput}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
                  placeholder="Ask, search, save, or email..."
                  rows={1}
                  disabled={showFiles}
                />
                <button 
                  className={styles.sendButton} 
                  onClick={handleSend} 
                  disabled={isLoading || showFiles}
                >
                  ➤
                </button>
              </>
            )}
          </div>
          {uploadStatus && <div className={styles.uploadToast}>{uploadStatus}</div>}
        </div>
      ) : (
        <div className={styles.chatbotIcon} onClick={() => setIsOpen(true)}>
          🤖
        </div>
      )}
    </div>
  );
};

export default Chatbot;