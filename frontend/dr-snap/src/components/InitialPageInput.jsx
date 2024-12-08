import React, { useState } from "react";
import "../styles/ChatInput.css";
import camera from "../assets/icons/camera.png";
import enter from "../assets/icons/enter.png";

const ChatInput = ({ onSubmit }) => {
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
    <form className="initial-page-input" onSubmit={handleSubmit}>
      <div className="textarea-container">
        <label htmlFor="image-upload" className="camera-button">
          <img src={camera} alt="Upload" />
        </label>
        <input
          id="image-upload"
          type="file"
          className="hidden-file-input"
          accept="image/*"
          onChange={(e) => setImage(e.target.files[0])}
        />
        <textarea
          className="chat-textarea"
          placeholder="간단한 증상과 함께 사진을 첨부해주세요"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button type="submit" className="submit-button">
          <img src={enter} alt="Upload" />
        </button>
      </div>
    </form>
  );
};

export default InitialPageInput;