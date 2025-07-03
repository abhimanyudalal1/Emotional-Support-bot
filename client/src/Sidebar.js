import React from 'react';
import './Sidebar.css';

function Sidebar() {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>Relie</h2>
      </div>
      <div className="sidebar-search">
        <input type="text" placeholder="Search or start new chat" />
      </div>
      <div className="sidebar-chats">
        <p className="sidebar-chat active">🧠 Relie Bot</p>
        {/* Add more static/future contacts here */}
      </div>
    </div>
  );
}

export default Sidebar;
