    # # Extract the ingredient name
    # words = recipe_text.split()
    # ingredient_name = words[-1]  # Assuming last word is the ingredient (Improve this later)

    # # Get ingredient details from DB
    # ingredient_data = collection.find_one({"name": ingredient_name})

    # if ingredient_data:
    #     predicted_type = ingredient_data.get("type")
    # else:
    #     # Predict missing details
    #     ingredient_name, predicted_density_ml, predicted_density_cup, category, predicted_type = predict_densities(ingredient_name)
    #     add_prediction_to_db(ingredient_name, predicted_density_ml, predicted_density_cup, predicted_type, category)