import React from "react";
import "../styles/Header.css";
import logo from "../assets/logo/logo.png";
import faqheader from "../assets/logo/faqheader.png"

const Header = ({currentPage}) => {
  return (
    <header className="header">
      <img 
        className="header-logo"
        src={currentPage === "faq" ? faqheader : logo} 
        alt={currentPage === "faq" ? "질문 이어가기" : "Dr.snap"}  
      />
    </header>
  );
};

export default Header;
