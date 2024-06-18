import numpy as np
from marshmallow import ValidationError
from flask import Blueprint, request, jsonify
from .schemas import ingredient_schema
from .models import model
from .utils import preprocess_ingredients, retrieve_recipes

main = Blueprint('main', __name__)

@main.errorhandler(ValidationError)
def handle_validation_error(error):
    response = jsonify({
        "status": "failed",
        "message": error.messages
    })
    response.status_code = 400
    return response

@main.route("/predict", methods=['POST'])
def predict():
    # Get data from POST request
    data = ingredient_schema.load(request.get_json(force=True))
    
    input_ingredients = data['ingredients']
    
    preprocessed_ingredients = preprocess_ingredients(input_ingredients)

    prediction = model.predict(preprocessed_ingredients)

    flatted_prediction = np.argsort(prediction).flatten()
    
    sorted_prediction = flatted_prediction[::-1]

    top_10_prediction = sorted_prediction[:10]
    
    recommended_recipes = retrieve_recipes(top_10_prediction)
    
    return jsonify({
        "status": "success",
        "data": recommended_recipes
    })

@main.route("/recipes", methods=['GET'])
def get_recipes():
    search=request.args.get('search')
    recipes = retrieve_recipes()
    if search : 
        recipes=[item for item in recipes if search.lower() in item["title"].lower()]
    return jsonify({
        "status": "success",
        "data": recipes
    })