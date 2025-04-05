import React, { useState } from "react";
import axios from "axios";
import { Bot, Sparkles } from "lucide-react";
import ReactMarkdown from "react-markdown";
import "./Converter.css";

function Converter() {
  const [inputText, setInputText] = useState("");
  const [result, setResult] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleConvert = async () => {
    setIsLoading(true);
    setTimeout(async () => {
      try {
        const response = await axios.post("http://localhost:5000/convert", {
          recipe_text: inputText, // key must match FastAPI model
        });
        console.log("Backend Response:", response.data);
        setResult(response.data.result); // Show message in chat
      } catch (error) {
        console.error("Error:", error);
        setResult("Error processing request");
      } finally {
        setIsLoading(false);
      }
    }, 1000);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;
    await handleConvert();
  };

  return (
    <div className="chat-container">
      <div className="chat-content">
        {/* Header */}
        <div className="chat-header">
          <Bot className="header-icon" />
          <h1>Gramify</h1>
        </div>

        {/* Chat Area */}
        <div className="chat-area">
          {isLoading && (
            <div className="loading-overlay">
              <div className="loading-content">
                <div className="spinner-container">
                  <div className="spinner"></div>
                  <Sparkles className="sparkle-icon" />
                </div>
                <p>Generating response...</p>
              </div>
            </div>
          )}
          {result && (
            <div className="response-message">
              <ReactMarkdown>{result}</ReactMarkdown>
            </div>
          )}
        </div>

        <div className="formula-note">
          <p>
            *Note these are the measurements taken into consideration <br />
            1 cup = 16 tbsp &nbsp; | &nbsp; 1 cup = 48 tsp &nbsp; | &nbsp; 1 cup = 240 ml &nbsp; | &nbsp;
            1 tbsp = 3 tsp &nbsp; | &nbsp; 1 tbsp = 15 ml &nbsp; | &nbsp; 1 tsp = 5 ml
          </p>
        </div>

        {/* Input Field */}
        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Enter your prompt here..."
            className="prompt-input"
            value={inputText}
          />
          <button type="submit" disabled={isLoading} className="submit-button">
            <Sparkles />
          </button>
        </form>
      </div>
    </div>
  );
}

export default Converter;
