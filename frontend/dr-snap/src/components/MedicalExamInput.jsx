import React from "react";
import "../styles/ChatInput.css";

const MedicalExamInput = ({ onSubmit }) => {
  return (
    <div className="medical-exam-input">
      <button className="o-button" onClick={() => onSubmit("O")}>
        O
      </button>
      <button className="x-button" onClick={() => onSubmit("X")}>
        X
      </button>
    </div>
  );
};

export default MedicalExamInput;