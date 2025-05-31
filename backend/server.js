const express = require("express");
const cors = require("cors");
const axios = require("axios");
const path = require("path");

const app = express();
app.use(express.json());
app.use(cors());

// Serve built frontend
app.use(express.static(path.join(__dirname, "frontend")));

// FastAPI Cloud Run endpoint
const FASTAPI_URL = "https://gramify-941292204609.asia-south1.run.app/convert";

app.post("/convert", async (req, res) => {
  const { recipe_text } = req.body;

  try {
    const response = await axios.post(FASTAPI_URL, { recipe_text });
    res.json({ result: response.data.message });
  } catch (error) {
    console.error("Error calling FastAPI:", error.message);
    res.status(500).json({ error: "Failed to get response from FastAPI." });
  }
});

// Fallback to index.html (for client-side routing)
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "frontend", "index.html"));
});

// Cloud Run expects port 8080
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
