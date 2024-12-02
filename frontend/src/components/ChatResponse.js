import React from 'react';

function ChatResponse({ userMessage, botMessage }) {
  return (
    <div className="chat-response">
      <div className="user-message">{userMessage}</div>
      <div className="bot-message">{botMessage}</div>
    </div>
  );
}

export default ChatResponse;
