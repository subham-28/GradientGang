from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import pymongo
# from main import extract_measurements  # Import but don't use globally

# Step 1: Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://aditya:gradientgang@cluster0.d11je.mongodb.net/")
db = client["baking_ai"]
collection = db["ingredients"]

# Function to get similar ingredients
def get_similar_ingredients(category):
    """Retrieve ingredients of the same category from MongoDB."""
    similar_items = list(collection.find({"category": category}, {"_id": 0}))
    return pd.DataFrame(similar_items)

#function to dtect solid or liq
def predict_type_by_density(density):
    return "Liquid" if density >= 0.9 else "Solid"

# Function to train and predict missing densities
def predict_densities(ingredient):
    """
    Predict density and grams per cup based on user input.
    """
    #_, _, ingredient = extract_measurements(user_text)  # Now safely using extract_measurements

    # Step 1: Retrieve category from DB
    # ingredient_data = collection.find_one({"name": ingredient.lower()})
    # if ingredient_data:
    #     return ingredient_data['density_g_per_ml']
    # else:
    from predict_category import get_ingredient_category
    category = get_ingredient_category(ingredient)

    # Step 1: Get similar ingredients
    df = get_similar_ingredients(category)
    if df.empty:  
        return {"error": f"No data found for ingredient category: {ingredient}"}

    # Step 2: Train ML Model
    X = df[["density_g_per_ml"]]  # Feature: Density (g/mL)
    y = df["grams_per_cup"]  # Target: Grams per Cup

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Step 3: Predict grams per cup using the average density
    avg_density = df["density_g_per_ml"].mean()
    predicted_grams_per_cup = model.predict([[avg_density]])[0]

    # Step 4: Return the correct density (which is the average of known densities)
    predicted_density_ml = avg_density  

    # Step 5: Identify if the ingredient is solid or liquid
    predicted_type = predict_type_by_density(predicted_density_ml)

    return ingredient,predicted_density_ml,predicted_grams_per_cup,category,predicted_type
    

# _,predicted_density_ml,_=predict_densities(user_text)



# Step 7: Optional - Store Prediction in Database
def add_prediction_to_db(ingredient_name, predicted_density, predicted_grams_per_cup, predicted_type,cate):
    new_ingredient = {
        "name": ingredient_name,
        "density_g_per_ml": predicted_density,
        "grams_per_cup": predicted_grams_per_cup,
        "category": cate,
        "type": predicted_type
    }
    collection.insert_one(new_ingredient)
    print(f"Inserted {ingredient_name} into database.")

# #Uncomment to store prediction in DB
# add_prediction_to_db(ingredient, predicted_density_ml, predicted_density_cup, predicted_type,cate)
