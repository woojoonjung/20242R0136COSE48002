import React, { useState } from "react";
import Header from "../components/Header.jsx";
import ChatResponse from "../components/ChatResponse.jsx";
import ChatInput from "../components/ChatInput.jsx";
import "../styles/index.css";
import { sendChatbotQuery } from "../services/api";

const ChatbotPage = () => {
  const [response, setResponse] = useState({ text: "", img_urls: [] });
  const [showInput, setShowInput] = useState(true);

  const handleQuerySubmit = async (text, image) => {
    try {
      setResponse({ text: "흠...", img_urls: [] });
      const backendResponse = await sendChatbotQuery(text, image);
      setResponse({
        text: backendResponse.response || "No response received.",
        img_urls: backendResponse.img_urls || [],
      });
      setShowInput(false);
    } catch (error) {
      console.error("Error communicating with the server:", error);
      setResponse({
        text: "Error: Unable to process your request.",
        img_urls: [],
      });
    }
  };

  return (
    <div className="chatbot-page">
      <Header />
      <ChatResponse response={response} />
      {showInput && <ChatInput onSubmit={handleQuerySubmit} />}
    </div>
  );
};

export default ChatbotPage;
