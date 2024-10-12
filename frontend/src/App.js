import React, {useState} from 'react';
import ChatInput from './components/ChatInput';
import ChatResponse from './components/ChatResponse';
import axios from 'axios';
import './App.css';

function App() {
  const [responses,setResponses] = useState([]);
  
  const handleSendMessage = async (message) => {
    try {
      const response = await axios.post('http://localhost:1001/api/message', { message });
      setResponses([...responses, { user: message, bot: response.data }]);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };
  

  return (
    <div className="chat-container">
      {responses.map((res, index) => (
        <ChatResponse key={index} userMessage={res.user} botMessage={res.bot} />
      ))}
      <ChatInput onSendMessage={handleSendMessage} />
    </div>
  );
}

export default App;