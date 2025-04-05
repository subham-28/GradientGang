import React from "react";
import "./About.css";

const About = () => {
  return (
    <section className="about-section">
      <div className="about-container">
        <h2 className="about-title">ABOUT</h2>
        <p className="about-text">
          Baking is all about precision, but online recipes often list
          ingredients in vague measurements like <b>"cups"</b> and{" "}
          <b>"spoons"</b>, leading to inconsistent results. That's where we come
          in! Our AI-powered platform converts these imprecise units into
          accurate <b>gram-based measurements</b>, ensuring perfect consistency
          in every recipe.
        </p>
        <p className="about-text">
          Using cutting-edge <b>Natural Language Processing (NLP)</b>,{" "}
          <b>Optical Character Recognition (OCR)</b>,{" "}
          <b>Machine Learning (ML)</b>, and a dynamic ingredient database, our
          solution adapts to your needs, whether you're a home baker or a
          professional chef.
        </p>
      </div>
    </section>
  );
};

export default About;
