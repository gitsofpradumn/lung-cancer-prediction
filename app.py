from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained ML pipeline
pipeline = joblib.load("lung_cancer_pipeline.pkl")

# Features used during model training
features = [
    "age",
    "gender",
    "education_years",
    "income_level",
    "smoker",
    "smoking_years",
    "cigarettes_per_day",
    "pack_years",
    "passive_smoking",
    "air_pollution_index",
    "occupational_exposure",
    "radon_exposure",
    "family_history_cancer",
    "copd",
    "asthma",
    "previous_tb",
    "bmi",
    "exercise_hours_per_week",
    "diet_quality",
    "alcohol_units_per_week",
    "healthcare_access"
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/test")
def test_model():
    return jsonify({
        "message": "Model loaded successfully!"
    })


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    input_data = {feature: data[feature] for feature in features}

    input_df = pd.DataFrame([input_data], columns=features)

    prediction = pipeline.predict(input_df)[0]
    probability = pipeline.predict_proba(input_df)[0][1]

    return jsonify({
        "prediction": int(prediction),
        "risk_score": round(float(probability) * 100, 2)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)