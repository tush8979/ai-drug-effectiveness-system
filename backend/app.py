from flask import Flask, request, jsonify
from flask_cors import CORS
from model.predict import rank_drugs
import requests
import json
import pandas as pd
import os
import re
import pdfplumber
from difflib import get_close_matches

app = Flask(__name__)
CORS(app)

# =========================
# LOAD CONDITIONS
# =========================
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data/processed/final_data.csv")

data = pd.read_csv(DATA_PATH)
data["condition"] = data["condition"].str.lower().str.strip()
ALL_CONDITIONS = sorted(data["condition"].unique())

# =========================
# 🔥 STRONG CLASSIFIER
# =========================
def classify_condition_llm(condition):
    condition = condition.lower()

    # 🔥 CRITICAL FIX
    if any(x in condition for x in ["cancer", "tumor", "carcinoma", "cance", "tum"]):
        return "critical"

    if any(x in condition for x in ["diabetes", "hypertension", "adhd"]):
        return "chronic"

    return "acute"


# =========================
# LLM EXPLANATION
# =========================
def analyze_drug_with_llm(drug, condition, age, bmi, severity):
    try:
        prompt = f"""
Condition: {condition}
Drug: {drug}

Explain in one sentence for patient age {age}, BMI {bmi}, severity {severity}.
JSON:
{{"safe": true, "reason": "..."}}
"""

        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=10
        )

        output = res.json().get("response", "")

        start = output.find("{")
        end = output.rfind("}") + 1
        parsed = json.loads(output[start:end])

        reason = parsed.get("reason", "")

        if len(reason.split()) < 6:
            reason = f"{drug} helps manage {condition} effectively."

        return {"safe": True, "reason": reason}

    except:
        return {"safe": True, "reason": f"{drug} is used for {condition}."}


# =========================
# PDF EXTRACTION
# =========================
def extract_text_from_pdf(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"

    return text.lower()


def extract_medical_values(text):
    def extract(pattern):
        match = re.search(pattern, text)
        return float(match.group(1)) if match else None

    return {
        "crp": extract(r"crp.*?(\d+\.?\d*)"),
        "esr": extract(r"esr.*?(\d+\.?\d*)"),
        "aso": "positive" if "aso titre positive" in text else None,
        "neutrophils": extract(r"neutrophils.*?(\d+)")
    }


def detect_condition_from_values(values):
    crp = values.get("crp") or 0
    esr = values.get("esr") or 0
    aso = values.get("aso")
    neut = values.get("neutrophils") or 0

    if aso == "positive" and crp > 100:
        return "streptococcal infection"

    if crp > 100 or esr > 50:
        return "severe infection"

    if neut > 70:
        return "bacterial infection"

    if crp > 10:
        return "infection"

    return "mild condition"


# =========================
# SUGGEST
# =========================
@app.route("/suggest", methods=["GET"])
def suggest():
    q = request.args.get("q", "").lower()
    return jsonify([c for c in ALL_CONDITIONS if q in c][:8])


# =========================
# 🔥 FINAL PREDICT (FIXED)
# =========================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        req = request.json or {}

        condition = req.get("condition", "")
        age = float(req.get("age", 30))
        bmi = float(req.get("bmi", 25))
        severity = float(req.get("severity", 5))

        # 🔥 MATCH FIX
        matched_condition = condition

        match = get_close_matches(condition.lower(), ALL_CONDITIONS, n=1, cutoff=0.5)

        if match:
            matched_condition = match[0]
        elif "cance" in condition:
            matched_condition = "cancer"
        elif "tum" in condition:
            matched_condition = "tumor"

        # 🔥 CLASSIFICATION FIX
        condition_type = classify_condition_llm(matched_condition)

        # 🔥 MAIN FIX
        results = rank_drugs(matched_condition, age, bmi, severity, condition_type)

        if not results:
            return jsonify({"status": "error", "message": "No drugs found"})

        final = []

        for r in results:
            llm = analyze_drug_with_llm(
                r["drug"], matched_condition, age, bmi, severity
            )

            final.append({
                "drug": r["drug"],
                "score": r["score"],
                "review_count": r.get("review_count", 0),
                "recovery_days": r["recovery_days"],
                "explanation": llm["reason"]
            })

        return jsonify({
            "status": "success",
            "best_drug": final[0]["drug"],
            "top_5": final
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# =========================
# REPORT
# =========================
@app.route("/analyze-report", methods=["POST"])
def analyze_report():
    try:
        file = request.files["file"]

        text = extract_text_from_pdf(file)
        values = extract_medical_values(text)
        condition = detect_condition_from_values(values)

        age, severity = 30, 5
        bmi = 25

        condition_type = classify_condition_llm(condition)

        results = rank_drugs(condition, age, bmi, severity, condition_type)

        final = []

        for r in results:
            llm = analyze_drug_with_llm(
                r["drug"], condition, age, bmi, severity
            )

            final.append({
                "drug": r["drug"],
                "score": r["score"],
                "review_count": r.get("review_count", 0),
                "recovery_days": r["recovery_days"],
                "explanation": llm["reason"]
            })

        return jsonify({
            "status": "success",
            "detected_condition": condition,
            "values": values,
            "best_drug": final[0]["drug"],
            "top_5": final
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)