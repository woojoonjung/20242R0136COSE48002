import React from "react";
import axios from "axios";
import "../styles/ChatResponse.css";

const ChatResponse = ({ response }) => {
  return (
    <div className="chat-response">
      {!response.text ? (
        <p className="default-text"> 어디가 불편하신가요? </p>
      ) : (
        <>
          {response.text && <p className="response-text">{response.text}</p>}
        </>
      )}
    </div>
  );
};

export default ChatResponse;