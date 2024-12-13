import React, { useState } from "react";
import Header from "../components/Header.jsx";
import ChatResponse from "../components/ChatResponse.jsx";
import ChatInput from "../components/ChatInput.jsx";
import "../styles/index.css";
import { sendChatbotQuery, sendMedicalExamResponse, sendFaqQuery } from "../services/api";

const ChatbotPage = () => {
  const [messages, setMessages] = useState([]);
  const [currentPage, setCurrentPage] = useState("initial");
  const [uploadedPreview, setUploadedPreview] = useState(null);
  const [submittedText, setSubmittedText] = useState("");
  const [thumbnailOpacity, setThumbnailOpacity] = useState(1);

  const handleQuerySubmit = async (text, image) => {
    setMessages([]);
    setSubmittedText(text);
    try {
      const userMessage = { type: "user", text: text };
      setMessages((prev) => [...prev, userMessage]);
      setMessages((prev) => [...prev, { type: "bot", text: "예상되는 병이 몇 가지 있는데요\n더 확실한 진단을 위해 몇 가지 질문드리겠습니다" }]);
      setThumbnailOpacity(0.5);
      setCurrentPage("loading");
      const backendResponse = await sendChatbotQuery(text, image);
      const botMessage = {
        type: "bot",
        text: backendResponse.response || "No response received.",
      };
      
      setMessages((prev) => [...prev, botMessage]);
      setCurrentPage("medicalExamination");
    } catch (error) {
      console.error("Error communicating with the server:", error);
      setMessages((prev) => [
        ...prev,
        { type: "bot", text: "Error: Unable to process your request." },
      ]);
    }
  };

  const UploadedContentContainer = ({ uploadedPreview, text, currentPage }) => {
    if (!uploadedPreview || (currentPage === "diagnosis" || currentPage === "faq")) {
      return null;
    }
  
    return (
      <div 
        className="uploaded-content-container" 
        style={{ 
          opacity: thumbnailOpacity,
          width: text ? "48.5%" : "auto",
          transition: "width 0.3s ease", 
        }}
      >
        <img 
          src={uploadedPreview} 
          alt="Uploaded Preview" 
          className="uploaded-thumbnail" 
        />
        {currentPage !== "initial" && <p className="uploaded-text">{text}</p>}
      </div>
    );
  };

  const handleMedicalExamSubmit = async (choice) => {
    setMessages((prev) => [...prev, { type: "user", text: choice }]);

    try {
      const backendResponse = await sendMedicalExamResponse(choice);
      if (backendResponse.diagnosis_finalized) {
        setMessages([{ type: "bot", text: backendResponse.response }]);
        setCurrentPage("diagnosis");
      } else {
        setMessages((prev) => [
          ...prev,
          { type: "bot", text: backendResponse.response },
        ]);
      }
    } catch (error) {
      console.error("Error handling medical exam response:", error);
      setMessages((prev) => [
        ...prev,
        { type: "bot", text: "Error processing your response." },
      ]);
    }
  };

  const handleNavigate = () => {
    console.log("Navigating to further FAQ...");
    setCurrentPage("faq");
  };

  const handleSave = () => {
    console.log("Saving the diagnosis log...");
    alert("진료가 저장되었습니다!");
  };

  const handleFAQSubmit = async (text, image) => {
    const userMessage = { type: "user", text: text };
    setMessages((prev) => [...prev, userMessage]);

    const backendResponse = await sendFaqQuery(text, image);
    const botMessage = {
      type: "bot",
      text: backendResponse.response || "No response received.",
    };
    setMessages((prev) => [...prev, botMessage]);
  };

  return (
    <div className="chatbot-page">
      <Header currentPage={currentPage} />
      <ChatResponse messages={messages} currentPage={currentPage} />
      <UploadedContentContainer
        uploadedPreview={uploadedPreview}
        text={submittedText}
        currentPage={currentPage}
      />
      <ChatInput
        currentPage={currentPage}
        onSubmit={
          currentPage === "initial"
            ? handleQuerySubmit
            : currentPage === "medicalExamination"
            ? handleMedicalExamSubmit
            : currentPage === "faq"
            ? handleFAQSubmit
            : null
        }
        setUploadedPreview={setUploadedPreview}
        onNavigate={handleNavigate}
        onSave={handleSave}
      />
    </div>
  );
};

export default ChatbotPage;
