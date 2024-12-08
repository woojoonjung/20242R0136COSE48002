import React, { useState } from "react";
import Header from "../components/Header.jsx";
import ChatResponse from "../components/ChatResponse.jsx";
import ChatInput from "../components/ChatInput.jsx";
import "../styles/index.css";
import { sendChatbotQuery, sendMedicalExamResponse } from "../services/api";

const ChatbotPage = () => {
  const [response, setResponse] = useState({ text: "" });
  const [currentPage, setCurrentPage] = useState("initial"); // Manage current page state, set "initial" initially

  const handleQuerySubmit = async (text, image) => {
    try {
      setResponse({ text: "흠..."});
      const backendResponse = await sendChatbotQuery(text, image);
      setResponse({
        text: backendResponse.response || "No response received.",
      });
      setCurrentPage("medicalExamination");
    } catch (error) {
      console.error("Error communicating with the server:", error);
      setResponse({
        text: "Error: Unable to process your request."
      });
    }
  };

  const handleMedicalExamSubmit = async (choice) => {
    try {
      const backendResponse = await sendMedicalExamResponse(choice)
  
      // Check if diagnosis is finalized
      if (backendResponse.data.diagnosis_finalized) {
        setResponse({ text: backendResponse.data.response });
        setCurrentPage("diagnosis"); // Transition to diagnosis page
      } else {
        setResponse({
          text: backendResponse.data.response,
        });
      }
    } catch (error) {
      console.error("Error handling medical exam response:", error);
      setResponse({ text: "Error processing your response." });
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

  return (
    <div className="chatbot-page">
      <Header />
      <ChatResponse response={response} />
      <ChatInput
        currentPage={currentPage}
        onSubmit={currentPage === "initial" ? handleQuerySubmit : handleMedicalExamSubmit}
        onNavigate={handleNavigate}
        onSave={handleSave}
      />
    </div>
  );
};

export default ChatbotPage;
