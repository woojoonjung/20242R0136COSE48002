import React from "react";
import "../styles/Header.css";
import logo from "../assets/logo/logo.png";

const Header = () => {
  return (
    <header className="header">
      <img src={logo} alt="Dr. Snap Logo" className="header-logo" />
    </header>
  );
};

export default Header;
