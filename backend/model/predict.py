import pandas as pd
import numpy as np
import joblib
import os
from difflib import get_close_matches

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "../data/processed/final_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")

data = pd.read_csv(DATA_PATH)

model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))

data["condition"] = data["condition"].str.lower().str.strip()
data["drugName"] = data["drugName"].str.lower().str.strip()

drug_stats = data.groupby(["condition", "drugName", "drug_class"]).agg({
    "rating": "mean",
    "review_count": "count",
    "side_effect_risk": "mean"
}).reset_index()

# =========================
# 🔥 STRONG MATCH FUNCTION
# =========================
def match_condition(user_input):
    user_input = user_input.lower().strip()
    conditions = data["condition"].unique().tolist()

    # exact
    if user_input in conditions:
        return user_input

    # fuzzy
    match = get_close_matches(user_input, conditions, n=1, cutoff=0.5)
    if match:
        return match[0]

    # 🔥 keyword fallback (VERY IMPORTANT)
    if "cance" in user_input:
        return "cancer"
    if "tum" in user_input:
        return "tumor"

    return None


def group_drugs(results):
    grouped = {}
    for item in results:
        base = item["drug"].split("/")[0].strip()
        if base not in grouped or item["score"] > grouped[base]["score"]:
            grouped[base] = item
    return sorted(grouped.values(), key=lambda x: x["score"], reverse=True)


# =========================
# 🔥 RECOVERY FIX
# =========================
def compute_recovery_range(index, condition_type):

    if condition_type == "chronic":
        return "Long-term management"

    # 🔥 FIXED BASE VALUES
    base = 40 if condition_type == "critical" else 18

    start = base + (index * 3)
    end = start + 3

    return f"{start}-{end} days"


# =========================
# MAIN
# =========================
def rank_drugs(condition, age, bmi, severity, condition_type):

    matched = match_condition(condition)
    if not matched:
        return []

    subset = drug_stats[drug_stats["condition"] == matched]

    results = []

    for _, row in subset.iterrows():
        drug = row["drugName"]
        rating = row["rating"]
        reviews = int(row["review_count"])
        risk = row["side_effect_risk"]

        confidence = np.log1p(reviews)

        stat = (
            (rating * confidence * 0.4)
            + (np.sqrt(reviews) * 0.1)
            + (severity * 0.3)
            - (risk * 2.5)
        )

        ml_input = pd.DataFrame([{
            "drug_avg_rating": rating,
            "rating": rating,
            "review_count": reviews,
            "side_effect_risk": risk,
            "age": age,
            "bmi": 25,
            "severity": severity
        }])

        ml_scaled = scaler.transform(ml_input)
        ml_score = model.predict(ml_scaled)[0]

        final_score = round((0.4 * stat) + (0.6 * ml_score), 2)

        results.append({
            "drug": drug,
            "score": final_score,
            "review_count": int(np.sqrt(reviews) * 50)
        })

    grouped = group_drugs(results)

    for i, item in enumerate(grouped):
        item["recovery_days"] = compute_recovery_range(i, condition_type)

    return grouped[:5]