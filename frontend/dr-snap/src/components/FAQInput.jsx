import React, { useState } from "react";
import camera from "../assets/icons/camera.png";
import enter from "../assets/icons/enter.png";

const FAQInput = ({ onSubmit }) => {
    const [text, setText] = useState("");
    const [image, setImage] = useState(null);
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (text || image) {
        setText("");
        setImage(null);
        await onSubmit(text, image);
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
                placeholder="편하게 질문해주세요 🩺"
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault(); // Prevents adding a new line
                    document.getElementById("submit-button").click();
                }
                }}
            />
            <button 
                id="submit-button" 
                type="submit" 
                className="transparent-button"
            >
                <img src={enter} alt="Submit" />
            </button>
            </div>
        </form>
    );
};

export default FAQInput;
