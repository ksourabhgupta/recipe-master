from flask import Flask, request, jsonify
import yaml
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

with open("recipes.yml", "r") as f:
    recipe_data = yaml.safe_load(f)

@app.route("/recipes", methods=["GET"])
def get_dishes():
    return jsonify(list(recipe_data.keys()))

@app.route("/get-ingredients", methods=["POST"])
def get_ingredients():
    data = request.get_json()
    dish = data.get("dish")
    people = int(data.get("people", 0))
    grams = int(data.get("gramsPerPerson", 0))

    if dish not in recipe_data:
        return jsonify({"error": "Invalid dish"}), 400

    total_grams = people * grams
    ingredients = {k: round(v * total_grams, 1) for k, v in recipe_data[dish].items()}
    return jsonify({"ingredients": ingredients})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

