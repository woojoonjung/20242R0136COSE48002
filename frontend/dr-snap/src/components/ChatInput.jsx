import React, { useState } from "react";
import InitialPageInput from "./InitialPageInput.jsx";
import MedicalExamInput from "./MedicalExamInput.jsx";
import DiagnosisPageInput from "./DiagnosisPageInput.jsx";
import FAQInput from "./FAQInput.jsx";

const ChatInput = ({ currentPage, onSubmit, setUploadedPreview, onNavigate, onSave }) => {
  if (currentPage === "initial") {
    return <InitialPageInput onSubmit={onSubmit} setUploadedPreview={setUploadedPreview} />;
  } else if (currentPage === "medicalExamination") {
    return <MedicalExamInput onSubmit={onSubmit} />;
  } else if (currentPage === "diagnosis") {
    return <DiagnosisPageInput onNavigate={onNavigate} onSave={onSave} />;
  } else if (currentPage === "faq") {
    return <FAQInput onSubmit={onSubmit} />;
  }
  return null;
};

export default ChatInput;