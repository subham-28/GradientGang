import nltk
import spacy
from nltk.corpus import stopwords
from textblob import TextBlob
from word2number import w2n
import re
from fractions import Fraction
import pymongo
from predict_missing_densities import predict_densities,add_prediction_to_db

#downloading the stopwords
nltk.download('stopwords')
nltk.download('punkt_tab')

import importlib.util

# Check if model is already installed
if importlib.util.find_spec("en_core_web_sm") is None:
    from spacy.cli import download
    download("en_core_web_sm")

# Now load it
nlp = spacy.load("en_core_web_sm")


UNIT_MAPPING = ['tsp', 'teaspoon', 't', 'teaspoon', 'tbsp', 'tablespoon', 'tbs', 'tablespoon','T', 'tablespoon', 'c', 'cup', 'fl oz', 'fluid ounce', 'pt', 'pint', 'qt', 'quart','gal', 'gallon', 'cp', 'cup', 'tablespon', 'tablespoon', 'teaspon', 'teaspoon','cups', 'cup', 'tbsps', 'tablespoon', 'tsps', 'teaspoon', 'g', 'gram', 'grams', 'gram',
'kg', 'kilogram', 'oz', 'ounce', 'lb', 'pound','t']


from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
client = MongoClient("mongodb+srv://aditya:gradientgang@cluster0.d11je.mongodb.net/")
db = client["baking_ai"]
collection = db["ingredients"]


#Loading the data from database into a dataframe
df=pd.DataFrame(list(collection.find()))
df['name'] = df['name'].str.lower()
#print(df['name'])


def parse_quantity(word: str) -> float:
    if not word:
        return None
    if '/' in word:
        num, denom = word.split('/')
        return float(num) / float(denom)
    try:
        return float(w2n.word_to_num(word))
    except (ValueError, AttributeError):
        return None


"""Converts number words to numerical values."""
def convert_text_numbers(text):
   
    words = text.split()
    converted_words = []
    for word in words:
        try:
            converted_words.append(str(w2n.word_to_num(word)))
        except ValueError:
            converted_words.append(word)
    return " ".join(converted_words)

def convert_fractions(text):
    """Converts fractions and mixed fractions to float numbers."""
    return re.sub(r'\b\d+\s*\d+/\d+\b|\b\d+/\d+\b', 
                  lambda x: str(float(sum(Fraction(s) for s in x.group().split()))), 
                  text)
    
def text_preprocessing(text):
    text=str(TextBlob(text).correct())    
    text=convert_fractions(text)
    text=convert_text_numbers(text)
    return text
    
def extract_measurements(text):
    text = convert_fractions(text)  # Convert "1/2" -> "0.5"
    text = convert_text_numbers(text)
    
    doc = nlp(text)
    quantity = None
    unit = None
    ingredient = []

    for token in doc:
        if token.like_num:  # Check if the token is a number (quantity)
            quantity = float(token.text)
        elif token.text.lower() in UNIT_MAPPING:
            unit = token.text.lower()
        elif token.pos_ in ["NOUN", "ADJ", "PROPN"]:  # Possible ingredient name
            ingredient.append(token.text.lower())
    ingredient_str=" ".join(ingredient)
    return quantity, unit, ingredient_str

def convert_to_grams(text):
    global df
    quantity,unit,ingredient=extract_measurements(text)
    print(quantity,unit,ingredient)
    #ing=ingredient
    #if ingredient in df['name']:
    if ingredient not in df['name'].values:
        ingredient, predicted_density_ml, predicted_density_cup,cate,predicted_type=predict_densities(ingredient)
        print(ingredient, predicted_density_ml, predicted_density_cup,cate,predicted_type)
        add_prediction_to_db(ingredient, predicted_density_ml, predicted_density_cup, predicted_type,cate)
        
        
        df = pd.DataFrame(list(collection.find()))
        df['name'] = df['name'].str.lower()
          
    if df.loc[df['name'] == ingredient, 'type'].str.lower().eq('solid').any():
            if unit in ["cup", "cups","c"]:
                return quantity * df.loc[df['name'] == ingredient, 'grams_per_cup'].values[0]

            elif unit in ["tbsp","tbs","tablespoon","tablespoons"]:
                return quantity * (df.loc[df['name'] == ingredient, 'grams_per_cup'].values[0])/16 # 1 cup = 16 tbsp
            elif unit in ["tsp","teaspoons","teaspoon",'t']:
                return quantity * (df.loc[df['name'] == ingredient, 'grams_per_cup'].values[0])/48  # 1 cup = 48 tsp
            elif unit in ["gram", "g"]:
                return quantity  # Already in grams
    else:
            if unit in ["cup", "cups","c"]:
                return quantity * 240
            elif unit in ["tbsp","tbs","tablespoon","tablespoons"]:
                return quantity * 240/16  # 1 cup = 16 tbsp
            elif unit in ["tsp","teaspoons","teaspoon"]:
                return quantity * 240/ 48  # 1 cup = 48 tsp
            elif unit in ["ml", "millilitre"]:
                return quantity
            
            
            
# recipe_text = "3 cups almond flour"
# quantity, unit, ingredient = extract_measurements(recipe_text)
# print(quantity, unit, ingredient)
# converted_weight = convert_to_grams(recipe_text)

# if converted_weight:
#     print(f"{quantity} {unit} of {ingredient} is approximately {converted_weight} grams.")
# else:
#     print("Could not convert the ingredient.")
