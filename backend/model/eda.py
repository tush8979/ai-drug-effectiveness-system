import pandas as pd

# ================================
# LOAD DATASETS
# ================================
train = pd.read_csv("../data/raw/drugsComTrain_raw.csv")
test = pd.read_csv("../data/raw/drugsComTest_raw.csv")
df = pd.concat([train, test])

sider = pd.read_csv("../data/raw/meddra_all_se.tsv", sep="\t", low_memory=False)
medicine = pd.read_csv("../data/raw/medicine_dataset.csv")

# ================================
# FUNCTION TO ANALYZE DATA
# ================================
def analyze(df, name):
    print(f"\n\n📊 DATASET: {name}")
    print("=" * 60)

    print("\n🔹 SHAPE")
    print(df.shape)

    print("\n🔹 COLUMNS")
    print(df.columns)

    print("\n🔹 DATA TYPES")
    print(df.dtypes)

    print("\n🔹 MISSING VALUES")
    print(df.isnull().sum().sort_values(ascending=False).head(10))

    print("\n🔹 SAMPLE DATA")
    print(df.head(3))


# ================================
# RUN ANALYSIS
# ================================
analyze(df, "Drug Reviews")
analyze(sider, "SIDER (Side Effects)")
analyze(medicine, "Medicine Dataset")


# ================================
# DRUG REVIEWS INSIGHTS
# ================================
print("\n\n🔥 DRUG REVIEWS INSIGHTS")
print("=" * 60)

print("\nTop Conditions:")
print(df["condition"].value_counts().head(10))

print("\nTop Drugs:")
print(df["drugName"].value_counts().head(10))

print("\nRating Distribution:")
print(df["rating"].describe())

# ================================
# 🔥 REVIEW COUNT ANALYSIS (VERY IMPORTANT)
# ================================
print("\n\n🔥 REVIEW COUNT ANALYSIS")
print("=" * 60)

# Count reviews per drug
review_counts = df.groupby("drugName").size().reset_index(name="review_count")

print("\nTop drugs by review count:")
print(review_counts.sort_values("review_count", ascending=False).head(10))

print("\nReview count stats:")
print(review_counts["review_count"].describe())

print("\nCheck for zero reviews:")
print((review_counts["review_count"] == 0).sum())

# ================================
# SIDE EFFECT INSIGHTS
# ================================
print("\n\n🔥 SIDE EFFECT INSIGHTS")
print("=" * 60)

# Check important columns
print("\nColumns in SIDER:")
print(sider.columns)

# Try to find drug column automatically
drug_cols = [col for col in sider.columns if "drug" in col.lower()]
print("\nPossible drug columns:", drug_cols)

# Count side effects per drug (approx)
if len(drug_cols) > 0:
    drug_col = drug_cols[0]

    side_effect_count = sider.groupby(drug_col).size().reset_index(name="side_effect_count")

    print("\nTop drugs with most side effects:")
    print(side_effect_count.sort_values("side_effect_count", ascending=False).head(10))


# ================================
# MEDICINE DATASET INSIGHTS
# ================================
print("\n\n🔥 MEDICINE DATASET INSIGHTS")
print("=" * 60)

print("\nColumns:")
print(medicine.columns)

print("\nSample:")
print(medicine.head(3))

# Try to find useful columns
possible_cols = [col for col in medicine.columns if "use" in col.lower() or "effect" in col.lower()]
print("\nUseful columns (usage/effects):", possible_cols)