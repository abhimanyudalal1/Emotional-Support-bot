import React, { useState, useEffect, useRef, useCallback } from 'react';
import './App.css';
import { v4 as uuidv4 } from 'uuid';
import EmojiPicker from 'emoji-picker-react';

function App() {
  const [userId] = useState(uuidv4());
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [chatHistory, setChatHistory] = useState([]);
  const [sidebarWidth, setSidebarWidth] = useState(300);
  const [darkMode, setDarkMode] = useState(true);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);

  const chatRef = useRef(null);
  const emojiRef = useRef(null);
  const isDragging = useRef(false);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    const history = JSON.parse(localStorage.getItem('relie_history')) || [];
    setChatHistory(history);

    if (history.length === 0) {
      setMessages([
        {
          sender: 'bot',
          text: "👋 Hi! I'm Relie, your emotional support assistant.\nI'm here to listen anytime 💙"
        }
      ]);
    }
  }, []);

  useEffect(() => {
    chatRef.current?.scrollTo(0, chatRef.current.scrollHeight);
  }, [messages]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (emojiRef.current && !emojiRef.current.contains(event.target)) {
        setShowEmojiPicker(false);
      }
    };
    if (showEmojiPicker) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showEmojiPicker]);

  const saveChatHistory = (newMessages) => {
    const history = JSON.parse(localStorage.getItem('relie_history')) || [];
    const newEntry = {
      id: uuidv4(),
      timestamp: new Date().toLocaleString(),
      messages: newMessages,
    };
    const updatedHistory = [newEntry, ...history];
    localStorage.setItem('relie_history', JSON.stringify(updatedHistory));
    setChatHistory(updatedHistory);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { sender: 'user', text: input };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setInput('');
    setShowEmojiPicker(false);

    try {
      const res = await fetch('https://relie-backend-zq69.onrender.com/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, message: input })
      });

      const data = await res.json();
      const botMsg = { sender: 'bot', text: data.response || '⚠️ No response from assistant.' };
      const newMessages = [...updatedMessages, botMsg];
      setMessages(newMessages);
      saveChatHistory(newMessages);
    } catch (error) {
      console.error("Send error:", error);
      const errorReply = {
        sender: 'bot',
        text: "⚠️ Couldn't connect to the support assistant. Please try again."
      };
      const newMessages = [...updatedMessages, errorReply];
      setMessages(newMessages);
      saveChatHistory(newMessages);
    }
  };

  const handlePromptSend = async (prompt) => {
    const userMsg = { sender: 'user', text: prompt };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setShowEmojiPicker(false);

    try {
      const res = await fetch('https://relie-backend-zq69.onrender.com/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, message: prompt })
      });

      const data = await res.json();
      const botMsg = { sender: 'bot', text: data.response || '⚠️ No response from assistant.' };
      const newMessages = [...updatedMessages, botMsg];
      setMessages(newMessages);
      saveChatHistory(newMessages);
    } catch (error) {
      console.error("Prompt send error:", error);
      const errorReply = {
        sender: 'bot',
        text: "⚠️ Prompt failed to send. Please try again."
      };
      const newMessages = [...updatedMessages, errorReply];
      setMessages(newMessages);
      saveChatHistory(newMessages);
    }
  };

  const resetChat = () => {
    setMessages([{
      sender: 'bot',
      text: "👋 Hi again! I'm here for you anytime. Feel free to talk to me 💙"
    }]);
  };

  const downloadChat = () => {
    const text = messages.map(
      msg => `${msg.sender === 'user' ? 'You' : 'Relie'}: ${msg.text}`
    ).join('\n\n');
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'relie_chat.txt';
    link.click();
  };

  const toggleDarkMode = () => setDarkMode(prev => !prev);

  const loadChatFromHistory = (id) => {
    const history = chatHistory.find(h => h.id === id);
    if (history) setMessages(history.messages);
  };

  const onDrag = useCallback((e) => {
    if (!isDragging.current || isMobile) return;
    const newWidth = e.clientX;
    if (newWidth > 200 && newWidth < 500) setSidebarWidth(newWidth);
  }, [isMobile]);

  const stopDrag = useCallback(() => {
    isDragging.current = false;
  }, []);

  useEffect(() => {
    document.addEventListener('mousemove', onDrag);
    document.addEventListener('mouseup', stopDrag);
    return () => {
      document.removeEventListener('mousemove', onDrag);
      document.removeEventListener('mouseup', stopDrag);
    };
  }, [onDrag, stopDrag]);

  const startDrag = () => { isDragging.current = true; };

  return (
    <div className={`app-container ${darkMode ? 'dark' : 'light'}`}>
      {!isMobile && (
        <>
          <div className="sidebar" style={{ width: `${sidebarWidth}px` }}>
            <div className="sidebar-header">Relie</div>
            <div className="sidebar-search">
              <input type="text" placeholder="Search or start a new chat" />
            </div>
            <div className="sidebar-chats">
              <p className="sidebar-chat active">🧠 Relie Bot</p>
              {chatHistory.map(chat => (
                <p key={chat.id} className="sidebar-chat" onClick={() => loadChatFromHistory(chat.id)}>
                  🗂 {chat.timestamp}
                </p>
              ))}
            </div>
          </div>
          <div className="resizer" onMouseDown={startDrag} />
        </>
      )}

      <div className="chat">
        <div className="chat-header">
          Relie 💬
          <div>
            <button onClick={resetChat}>🗑</button>
            <button onClick={downloadChat}>💾</button>
            <button onClick={toggleDarkMode}>{darkMode ? '🌞' : '🌙'}</button>
          </div>
        </div>

        {showEmojiPicker && (
          <div className="emoji-picker" ref={emojiRef}>
            <EmojiPicker
              theme={darkMode ? 'dark' : 'light'}
              onEmojiClick={(emojiData) => {
                setInput(prev => prev + emojiData.emoji);
              }}
            />
          </div>
        )}

        <div className="chat-box" ref={chatRef}>
          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.sender}`}>
              <p>{msg.text}</p>
            </div>
          ))}
        </div>

        <div className="prompt-suggestions">
          {["I'm feeling stressed", "Give me motivation", "I need help sleeping", "Tell me a joke", "What can you do?"].map((prompt, idx) => (
            <button key={idx} className="prompt-btn" onClick={() => handlePromptSend(prompt)}>
              {prompt}
            </button>
          ))}
        </div>

        <div className="input-bar">
          <button onClick={() => setShowEmojiPicker(prev => !prev)}>😊</button>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Type a message"
            onKeyDown={e => e.key === 'Enter' && sendMessage()}
          />
          <button onClick={sendMessage}>➤</button>
        </div>
      </div>
    </div>
  );
}

export default App;
