import React from "react";
import "../styles/ChatInput.css";

const DiagnosisPageInput = ({ onNavigate, onSave }) => {
  return (
    <div className="diagnosis-page-input">
      <button className="continue-button" onClick={onNavigate}>
        질문 이어가기
      </button>
      <button className="save-button" onClick={onSave}>
        진료 저장하기
      </button>
    </div>
  );
};

export default DiagnosisPageInput;
