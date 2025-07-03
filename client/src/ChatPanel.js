import React, { useState, useEffect, useRef } from 'react';
import './ChatPanel.css';
import { v4 as uuidv4 } from 'uuid';

function ChatPanel() {
  const [userId] = useState(uuidv4());
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const chatRef = useRef(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');

    try {
      const res = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, message: input })
      });

      const data = await res.json();
      const botMsg = { sender: 'bot', text: data.response };
      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      const botMsg = {
        sender: 'bot',
        text: "⚠️ Couldn't connect. Please check the server."
      };
      setMessages(prev => [...prev, botMsg]);
    }
  };

  useEffect(() => {
    chatRef.current?.scrollTo(0, chatRef.current.scrollHeight);
  }, [messages]);

  return (
    <div className="chat">
      <div className="chat-header">Relie Bot</div>
      <div className="chat-body" ref={chatRef}>
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
          placeholder="Type a message"
        />
        <button onClick={sendMessage}>➤</button>
      </div>
    </div>
  );
}

export default ChatPanel;
