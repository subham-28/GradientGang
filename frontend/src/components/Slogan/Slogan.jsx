import React, { useEffect, useRef } from "react";
import "./Slogan.css";

const Slogan = () => {
  const sloganRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          sloganRef.current.classList.add("show");
          sloganRef.current.classList.remove("hide");
        } else {
          sloganRef.current.classList.add("hide");
        }
      },
      { threshold: 0.2 } 
    );

    if (sloganRef.current) {
      observer.observe(sloganRef.current);
    }

    return () => {
      if (sloganRef.current) observer.unobserve(sloganRef.current);
    };
  }, []);

  return (
    <div className="slogan hide" ref={sloganRef}>
      <h2 className="slogan-text">
        <i>Cup or Spoon? Let AI handle the conversion for perfect results!</i>
      </h2>
    </div>
  );
};

export default Slogan;
