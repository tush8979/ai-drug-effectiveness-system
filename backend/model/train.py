import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "../data/processed/final_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

df["condition"] = df["condition"].str.lower().str.strip()
df["drugName"] = df["drugName"].str.lower().str.strip()

# =========================
# DRUG AVG FEATURE
# =========================
drug_avg = df.groupby("drugName")["rating"].mean().reset_index()
drug_avg.columns = ["drugName", "drug_avg_rating"]

df = df.merge(drug_avg, on="drugName", how="left")

# =========================
# TARGET
# =========================
df["effectiveness"] = (
    0.6 * df["drug_avg_rating"]
    + 0.2 * df["rating"]
    + 0.1 * np.log1p(df["review_count"])
    - 0.3 * df["side_effect_risk"]
)

# reduce size
top_drugs = df["drugName"].value_counts().head(50).index
df = df[df["drugName"].isin(top_drugs)]

df = df.sample(30000, random_state=42)

# features
X = df[[
    "drug_avg_rating",
    "rating",
    "review_count",
    "side_effect_risk",
    "age",
    "bmi",
    "severity"
]]

y = df["effectiveness"]

# scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))

# model
model = XGBRegressor(
    n_estimators=120,
    max_depth=6,
    learning_rate=0.08,
    subsample=0.8,
    colsample_bytree=0.8,
    n_jobs=-1,
    random_state=42
)

print("🚀 Training...")
model.fit(X_scaled, y)

joblib.dump(model, os.path.join(MODEL_DIR, "model.pkl"))

print("✅ Done!")