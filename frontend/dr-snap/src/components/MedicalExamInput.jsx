import React from "react";
import "../styles/ChatInput.css";
import oImage from "../assets/icons/O.png";
import xImage from "../assets/icons/X.png"

const MedicalExamInput = ({ onSubmit }) => {
  return (
    <div className="medical-exam-input">
      <button className="o-button" onClick={() => onSubmit("O")}>
        <img src={oImage} alt="O" />
      </button>
      <button className="x-button" onClick={() => onSubmit("X")}>
        <img src={xImage} alt="X" />
      </button>
    </div>
  );
};

export default MedicalExamInput;