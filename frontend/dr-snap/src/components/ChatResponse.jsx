import React from "react";
import axios from "axios"; // Import axios to send data to the server
import "../styles/ChatResponse.css";

const ChatResponse = ({ response }) => {
  const handleImageClick = async (imgUrl) => {
    try {
      const API_URL = "http://localhost:49529";
      await axios.post(`${API_URL}/click`, { img_url: imgUrl });
      alert(`Image clicked: ${imgUrl}`);
    } catch (error) {
      console.error("Error sending image click data:", error);
    }
  };

  return (
    <div className="chat-response">
      {!response.text && !response.img_urls.length ? (
        <p className="default-text"> 어디가 불편하신가요? </p>
      ) : (
        <>
          {response.text && <p className="response-text">{response.text}</p>}
          {response.img_urls && response.img_urls.length > 0 && (
            <div className="image-container">
              {response.img_urls.map((url, index) => (
                <img
                  key={index}
                  src={url}
                  alt={`Response image ${index + 1}`}
                  className="response-image"
                  onClick={() => handleImageClick(url)} // Handle image click
                />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default ChatResponse;