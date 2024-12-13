import React, { useEffect, useRef } from "react";
import "../styles/ChatResponse.css";
import logo from "../assets/logo/logo.png";

const ChatResponse = ({ messages, currentPage }) => {
  const chatWindowRef = useRef(null);

  // Automatically scroll to the bottom when messages update
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  if (currentPage === "faq") {
    return (
      <div className="chat-response-container">
        <div className="chat-response chat-interface" ref={chatWindowRef}>
          {(
            messages.map((msg, index) => (
              <div
                key={index}
                className={`chat-message ${msg.type === "user" ? "user-message" : "bot-message"}`}
              >
                {msg.type === "bot" && (
                  <div>
                    <img src={logo} alt="Dr.Snap" className="bot-logo" />
                  </div>                  
                )}
                {msg.text.split("\n").slice(2 + parseInt(msg.text.split("\n")[1], 10))}
              </div>
            ))
          )}
        </div>
      </div>
    );
  }

  // Single-response logic for other pages
  const latestMessage = messages.length > 0 ? messages[messages.length - 1].text : "";
  const splitLatestMessage = (latestMessage) => {
    const lines = latestMessage.split("\n").map((line) => line.trim());
    const variableText = lines[0];
    const diagnosisPoints = lines.slice(2, 2 + parseInt(lines[1], 10));
    const diagnosis = lines.slice(2 + parseInt(lines[1], 10));
    return { variableText, diagnosisPoints, diagnosis };
  };
  const { variableText, diagnosisPoints, diagnosis } = splitLatestMessage(latestMessage)
  
  const DiagnosisSummary = ({ diagnosisPoints, variableText }) => {
    const sanitizedPoints = diagnosisPoints.map((point) => point.replace(/^- /, ""));
    return (
      <div className="diagnosis-summary-container">
        <div className="diagnosis-circles">
          {sanitizedPoints.map((point, index) => (
            <div key={index} className="diagnosis-circle">
              {point}
            </div>
          ))}
        </div>
        <p className="diagnosis-variable-text">
          위와 같은 증상을 보이는 것으로 보아 환자분의 질병은 <b>{variableText}</b>인 것으로 보입니다.
        </p>
      </div>
    );
  };

  return (
    <div className="chat-response">
      {!latestMessage ? (
        <div className="viewport-centered-container">
          <p className="default-text">어디가 불편하신가요?</p>
        </div>
      ) : (
        <div className={'viewport-centered-container ${currentPage === "diagnosis" ? "diagnosis" : ""}'}>
          {currentPage === "diagnosis" ? (
            <>
              <DiagnosisSummary
                diagnosisPoints={diagnosisPoints}
                variableText={variableText}
              />
              <p className="response-text diagnosis-response">
                {diagnosis.map((line, index) => (
                  <React.Fragment key={index}>
                    {line}
                    <br />
                  </React.Fragment>
                ))}
              </p>
            </>
          ) : (
            <p className="response-text">
              {latestMessage.split("\n").map((line, index) => (
                <React.Fragment key={index}>
                  {line}
                  <br />
                </React.Fragment>
              ))}
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default ChatResponse;
