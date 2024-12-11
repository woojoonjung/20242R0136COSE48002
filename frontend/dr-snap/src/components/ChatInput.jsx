import React, { useState } from "react";
import InitialPageInput from "./InitialPageInput.jsx";
import MedicalExamInput from "./MedicalExamInput.jsx";
import DiagnosisPageInput from "./DiagnosisPageInput.jsx";
import camera from "../assets/icons/camera.png";
import enter from "../assets/icons/enter.png";

const ChatInput = ({ currentPage, onSubmit, onNavigate, onSave }) => {
  if (currentPage === "initial") {
    return <InitialPageInput onSubmit={onSubmit} />;
  } else if (currentPage === "medicalExamination") {
    return <MedicalExamInput onSubmit={onSubmit} />;
  } else if (currentPage === "diagnosis") {
    return <DiagnosisPageInput onNavigate={onNavigate} onSave={onSave} />;
  } else if (currentPage === "faq") {
    const [text, setText] = useState("");
    const [image, setImage] = useState(null);
    const handleSubmit = (e) => {
      e.preventDefault();
      if (text || image) {
        onSubmit(text, image);
        setText(""); 
        setImage(null); 
      }
    };

    return (
      <form className="chat-input" onSubmit={handleSubmit}>
        <div className="textarea-container">
          <button
            type="button"
            className="transparent-button"
            onClick={() => document.getElementById('image-upload').click()}
          >
            <img src={camera} alt="Upload" />
          </button>
          <input
            id="image-upload"
            type="file"
            className="hidden-file-input"
            accept="image/*"
            onChange={(e) => setImage(e.target.files[0])}
          />
          <textarea
            className="chat-textarea"
            placeholder="편하게 질문해주세요 :)"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <button type="submit" className="transparent-button">
            <img src={enter} alt="Upload" />
          </button>
        </div>
      </form>
    );
  }
  return null;
};

export default ChatInput;
