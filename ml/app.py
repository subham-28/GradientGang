from fastapi import FastAPI
from pydantic import BaseModel
from main import convert_to_grams
from predict_missing_densities import predict_densities, add_prediction_to_db
from pymongo import MongoClient
import os
import uvicorn
# Initialize FastAPI app
app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb+srv://aditya:gradientgang@cluster0.d11je.mongodb.net/")
db = client["baking_ai"]
collection = db["ingredients"]

# Request body model
class IngredientInput(BaseModel):
    recipe_text: str  # Example: "2 cups of coconut flour"

@app.post("/convert/")
async def convert_ingredient(input_data: IngredientInput):
    recipe_text = input_data.recipe_text.lower()  # Convert to lowercase
    converted_weight = convert_to_grams(recipe_text)

    # Extract the ingredient name
    words = recipe_text.split()
    ingredient_name = words[-1]  # Assuming last word is the ingredient (Improve this later)

    # Get ingredient details from DB
    ingredient_data = collection.find_one({"name": ingredient_name})

    if ingredient_data:
        predicted_type = ingredient_data.get("type")
    else:
        # Predict missing details
        ingredient_name, predicted_density_ml, predicted_density_cup, category, predicted_type = predict_densities(ingredient_name)
        add_prediction_to_db(ingredient_name, predicted_density_ml, predicted_density_cup, predicted_type, category)

    # Format response
    if converted_weight:
        if predicted_type in ["Solid", "solid"]:
            return {"message": f"{recipe_text} weighs approximately {converted_weight:.2f} grams."}
        elif predicted_type in ["Liquid", "liquid"]:
            return {"message": f"{recipe_text} is approximately {converted_weight:.2f} milliliters."}
    return {"message": "Could not convert the ingredient."}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Cloud Run provides PORT=8080
    uvicorn.run("app:app", host="0.0.0.0", port=port)
