import pickle
import json
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
from dotenv import load_dotenv

load_dotenv()

tokenizer_path = './dist/tokenizer.pickle'
data_path = "./dist/recipes.json"

with open(tokenizer_path, 'rb') as handle:
    tokenizer = pickle.load(handle)
    
with open(data_path, 'r') as file:
    data = json.load(file)
    data = [{'id': index, 'imgUrl': x['IMG URL'], 'ingredients': x['Ingredients'], 'steps': x['Steps'], 'title': x['Title']} for index, x in enumerate(data)]

max_seq_length = int(os.getenv("MAX_SEQ_LEN"))

def preprocess_text(text):
    text = ' '.join(text)
    text = text.strip()  # Menghapus spasi di awal dan akhir teks
    return text

def preprocess_ingredients(input_ingredients):
    input_ingredients = preprocess_text(input_ingredients)
    input_sequence = tokenizer.texts_to_sequences([input_ingredients])
    input_padded = pad_sequences(input_sequence, maxlen=max_seq_length, padding='post')
    return input_padded

def retrieve_recipes(indexes=[]):
    if len(indexes)>0:
        recipes = [data[index] for index in indexes if index < 145]
    else:
        recipes = data
    return recipes