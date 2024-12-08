import React from "react";
import InitialPageInput from "./InitialPageInput.jsx";
import MedicalExamInput from "./MedicalExamInput.jsx";
import DiagnosisPageInput from "./DiagnosisPageInput.jsx";

const ChatInput = ({ currentPage, onSubmit, onNavigate, onSave }) => {
  if (currentPage === "initial") {
    return <InitialPageInput onSubmit={onSubmit} />;
  } else if (currentPage === "medicalExamination") {
    return <MedicalExamInput onSubmit={onSubmit} />;
  } else if (currentPage === "diagnosis") {
    return <DiagnosisPageInput onNavigate={onNavigate} onSave={onSave} />;
  }
  return null;
};

export default ChatInput;
