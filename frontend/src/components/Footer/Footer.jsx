import React from "react";
import "./Footer.css";
import { FaFacebook, FaTwitter, FaInstagram, FaLinkedin } from "react-icons/fa";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-logo">
          <h2>Gramify</h2>
          <p>Your AI-powered cooking assistant</p>
        </div>

        <div className="footer-links">
          <h3>Quick Links</h3>
          <ul className="footer-ul">
            <li>Home</li>
            <li>About</li>
            <li>Features</li>
            <li>Contact</li>
          </ul>
        </div>

        <div className="footer-social">
          <h3>Follow Us</h3>
          <ul className="social-icons">
            <li><FaFacebook /></li>
            <li><FaTwitter /></li>
            <li><FaInstagram /></li>
            <li><FaLinkedin /></li>
          </ul>
        </div>
      </div>

      <div className="footer-bottom">
        <p>© 2025 Gramify. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
