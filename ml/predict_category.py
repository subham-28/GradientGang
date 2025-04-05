from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from textblob import TextBlob
from pymongo import MongoClient


client = MongoClient("mongodb+srv://aditya:gradientgang@cluster0.d11je.mongodb.net/")
db = client["baking_ai"]
collection = db["ingredients"]

def get_ingredient_category(ingredient_name):
    """Predicts the category of a new ingredient using KNN on existing database."""
    
    # Load ingredients and categories from MongoDB
    df = pd.DataFrame(list(collection.find({}, {"_id": 0, "name": 1, "category": 1})))
    
    if df.empty:
        print("No data found in the database.")
        return None

    # Train KNN model
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["name"])  # Convert ingredient names into TF-IDF features
    y = df["category"]

    model = KNeighborsClassifier(n_neighbors=3)  # Use 3 nearest neighbors
    model.fit(X, y)

    # Predict category for new ingredient
    new_ingredient_vec = vectorizer.transform([ingredient_name])
    predicted_category = model.predict(new_ingredient_vec)[0]

    return predicted_category

# Example Usage
# new_ingredient = "coconut flour"  # Misspelled ingredient
# predicted_category = get_ingredient_category(new_ingredient)
# print(f"Predicted Category for '{new_ingredient}': {predicted_category}")
