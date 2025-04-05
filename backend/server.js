const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();
app.use(express.json());
app.use(cors());

// FastAPI endpoint
const FASTAPI_URL = "http://127.0.0.1:8000/convert/";

app.post("/convert", async (req, res) => {
  const { recipe_text } = req.body;

  try {
    // Send POST request to FastAPI server
    const response = await axios.post(FASTAPI_URL, { recipe_text });

    // Send the FastAPI response back to client
    res.json({ result: response.data.message });
  } catch (error) {
    console.error("Error calling FastAPI:", error.message);
    res.status(500).json({ error: "Failed to get response from FastAPI." });
  }
});

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
