import React from "react";
import "../styles/ChatResponse.css";

const ChatResponse = ({ messages, currentPage }) => {
  if (currentPage === "faq") {
    return (
      <div className="chat-response chat-interface">
        {messages.length === 0 ? (
          <p className="default-text">더 궁금하신게 있나요?</p>
        ) : (
          messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-message ${msg.type === "user" ? "user-message" : "bot-message"}`}
            >
              {msg.text}
            </div>
          ))
        )}
      </div>
    );
  }

  // Single-response logic for other pages
  const latestMessage = messages.length > 0 ? messages[messages.length - 1].text : "";

  return (
    <div className="chat-response">
      {!latestMessage ? (
        <p className="default-text">어디가 불편하신가요?</p>
      ) : (
        <>
          <p
            className={`response-text ${
              currentPage === "diagnosis" ? "diagnosis-response" : ""
            }`}
          >
            {latestMessage}
          </p>
          {currentPage === "diagnosis" && (
            <p className="additional-response">
              진단 결과를 자세히 확인하세요. 추가 정보는 질문 이어가기를 통해 확인할 수 있습니다.
            </p>
          )}
        </>
      )}
    </div>
  );
};

export default ChatResponse;
