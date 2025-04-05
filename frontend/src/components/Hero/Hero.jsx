import React from "react";
import "./Hero.css";
import { assets } from "../../assets/assets";
import { useNavigate } from "react-router-dom";

const Hero = () => {
  const navigate = useNavigate();
  return (
    <div className="Hero">
      <div className="hero-text">
        <h1>EASILY CONVERT YOUR MEASUREMENTS IN SECONDS</h1>
        <p>
          Transform your cooking experience with our simple tool. No more
          guesswork - get precise measurements every time.
        </p>
        <div className="hero-buttons">
          <button className="btn convert-btn" onClick={()=> navigate("/convert-units")}>Convert</button>
          <button className="btn learn-btn">Learn more</button>
        </div>
      </div>
      <div className="hero-image">
        <img src={assets.foodImg} alt="Delicious Food" />
      </div>
    </div>
  );
};

export default Hero;
