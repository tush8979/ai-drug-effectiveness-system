import pandas as pd
import numpy as np

# =========================
# LOAD DATA
# =========================
train = pd.read_csv("../data/raw/drugsComTrain_raw.csv")
test = pd.read_csv("../data/raw/drugsComTest_raw.csv")

df = pd.concat([train, test])

medicine = pd.read_csv("../data/raw/medicine_dataset.csv", low_memory=False)

# =========================
# CLEAN DRUG REVIEWS
# =========================
df = df[["drugName", "condition", "rating"]]
df = df.dropna()

df["drugName"] = df["drugName"].str.lower().str.strip()
medicine["name"] = medicine["name"].str.lower().str.strip()

# =========================
# REVIEW COUNT
# =========================
review_counts = df.groupby("drugName").size().reset_index(name="review_count")
df = df.merge(review_counts, on="drugName", how="left")

# =========================
# SIDE EFFECT RISK (REAL)
# =========================
side_cols = [col for col in medicine.columns if "sideEffect" in col]

medicine["side_effect_count"] = medicine[side_cols].notna().sum(axis=1)

medicine["side_effect_risk"] = (
    medicine["side_effect_count"] / medicine["side_effect_count"].max()
)

# =========================
# DRUG CLASS (VERY IMPORTANT)
# =========================
medicine["drug_class"] = medicine["Therapeutic Class"]\
    .fillna("unknown")\
    .str.lower()\
    .str.strip()

medicine = medicine[[
    "name",
    "side_effect_risk",
    "drug_class"
]]

# =========================
# MERGE
# =========================
df = df.merge(medicine, left_on="drugName", right_on="name", how="left")

df["side_effect_risk"] = df["side_effect_risk"].fillna(0.3)
df["drug_class"] = df["drug_class"].fillna("unknown")

# =========================
# PATIENT FEATURES
# =========================
np.random.seed(42)

df["age"] = np.random.randint(18, 80, len(df))
df["severity"] = np.random.randint(1, 10, len(df))
df["bmi"] = np.random.uniform(18, 35, len(df))

# =========================
# FINAL CLEAN
# =========================
df = df.drop(columns=["name"], errors="ignore")

# =========================
# SAVE
# =========================
df.to_csv("../data/processed/final_data.csv", index=False)

print("✅ Preprocessing COMPLETE (clean + class-based)")
print(df.head())
print("\nShape:", df.shape)