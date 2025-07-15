from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Load recipe data from CSV
df = pd.read_csv("recipe_data.csv")

@app.route("/recipes", methods=["GET"])
def get_dishes():
    dishes = df['Dish'].unique().tolist()
    return jsonify(dishes)

@app.route("/get-ingredients", methods=["POST"])
def get_ingredients():
    data = request.get_json()
    dish = data.get("dish")
    people = int(data.get("people", 0))
    grams = int(data.get("gramsPerPerson", 0))

    if not dish or people <= 0 or grams <= 0:
        return jsonify({"error": "Invalid input"}), 400

    # Filter ingredients for the selected dish, exclude 'Yield'
    filtered = df[(df["Dish"] == dish)]# & (df["Ingredient"] != "Yield")]

    total_grams = (people * grams)/1000

    ingredients = {}
    for _, row in filtered.iterrows():
        qty = float(row["quantity"]) * total_grams  # Scale up
        unit = row["unit"]
        ingredients[row["Ingredient"]] = f"{round(qty, 2)} {unit}"

    return jsonify({"ingredients": ingredients})


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# if __name__ == '__main__':
#     app.run(debug=True)

