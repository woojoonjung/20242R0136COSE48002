import React, { useState } from 'react';
import logo from './logo.png'; // 로고 이미지 경로
import ChatInput from './components/ChatInput';
import ChatResponse from './components/ChatResponse';
import axios from 'axios';
import './App.css';

function App() {
  const [responses, setResponses] = useState([]);
  const [image, setImage] = useState(null); // 이미지 상태 추가

  const handleSendMessage = async (message) => {
    const formData = new FormData();
    formData.append('symptoms', message);
    if (image) {
      formData.append('image', image); // 선택된 이미지 추가
    }

    try {
      const response = await axios.post('http://localhost:7776/prompt/message', formData, {
        headers: {
          'Content-Type': 'multipart/form-data', // multipart/form-data로 설정
        },
      });
      setResponses([...responses, { user: message, bot: response.data }]);
      setImage(null); // 메시지 전송 후 이미지 초기화
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const handleImageChange = (event) => {
    setImage(event.target.files[0]); // 선택된 이미지 상태 업데이트
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} alt="Project Logo" className="project-logo" />
      </header>

      <div className="chat-container">
        {responses.map((res, index) => (
          <ChatResponse key={index} userMessage={res.user} botMessage={res.bot} />
        ))}

        {/* 이미지 입력 영역 */}
        <div className="image-input-container">
          <input
            type="file"
            accept="image/*" // 이미지 파일만 선택 가능
            onChange={handleImageChange} // 이미지 변경 시 핸들러
            className="image-input" // 추가된 이미지 입력 클래스
          />
        </div>

        {/* 채팅 입력 영역 */}
        <div className="chat-input">
          <ChatInput onSendMessage={handleSendMessage} />
        </div>
      </div>
    </div>
  );
}

export default App;