from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "model" / "spam_model.pkl"
BACKEND_PATH = BASE_DIR / "backend"

sys.path.append(str(BACKEND_PATH))

from scam_detector import check_scam_risk

app = Flask(__name__)
CORS(app)

model = joblib.load(MODEL_PATH)


@app.route("/")
def home():
    return jsonify({
        "message": "AI Email Spam & Scam Detector API is running"
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "email" not in data:
        return jsonify({
            "error": "Please provide email text"
        }), 400

    email = data["email"].strip()

    if not email:
        return jsonify({
            "error": "Email cannot be empty"
        }), 400

    prediction = model.predict([email])[0]
    probabilities = model.predict_proba([email])[0]

    spam_probability = probabilities[1]
    legitimate_probability = probabilities[0]

    scam_result = check_scam_risk(email)

    if scam_result["risk"] == "High":
        final_prediction = "Potentially Fraudulent"
        final_risk = "High"

    elif prediction == 1:
        final_prediction = "Spam"
        final_risk = "Medium"

    else:
        final_prediction = "Legitimate"
        final_risk = scam_result["risk"]

    if prediction == 1:
        confidence = spam_probability * 100
    else:
        confidence = legitimate_probability * 100

    return jsonify({
        "prediction": final_prediction,
        "confidence": round(confidence, 2),
        "risk": final_risk,
        "scam_score": scam_result["score"],
        "reasons": scam_result["reasons"]
    })