import React, { useState } from "react";
import Header from "../components/Header.jsx";
import ChatResponse from "../components/ChatResponse.jsx";
import ChatInput from "../components/ChatInput.jsx";
import "../styles/index.css";
import { sendChatbotQuery, sendMedicalExamResponse } from "../services/api";

const ChatbotPage = () => {
  const [messages, setMessages] = useState([]);
  const [currentPage, setCurrentPage] = useState("initial");

  const handleQuerySubmit = async (text, image) => {
    setMessages([{ type: "bot", text: "예상되는 병이 몇 가지 있는데요 더 확실한 진단을 위해 몇 가지 질문드리겠습니다" }]);

    try {
      const userMessage = { type: "user", text: text };
      setMessages((prev) => [...prev, userMessage]);

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
    setCurrentPage("faq"); // Transition to the FAQ page
  };

  const handleSave = () => {
    console.log("Saving the diagnosis log...");
    // Logic to save the conversation log to local storage
    alert("진료가 저장되었습니다!");
  };

  const handleFAQSubmit = (text, image) => {
    const userMessage = { type: "user", text: text };
    setMessages((prev) => [...prev, userMessage]);

    const backendResponse = sendFaqQuery(text, image);
    const botMessage = {
      type: "bot",
      text: backendResponse.response || "No response received.",
    };
    setMessages((prev) => [...prev, botMessage]);
  };

  return (
    <div className="chatbot-page">
      <Header />
      <ChatResponse messages={messages} currentPage={currentPage} />
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
        onNavigate={handleNavigate}
        onSave={handleSave}
      />
    </div>
  );
};

export default ChatbotPage;
