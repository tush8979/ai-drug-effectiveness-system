import pandas as pd

df = pd.read_csv("../data/processed/final_data.csv")

print("\n🔥 CHECK DRUG VARIATION PER CONDITION")
print("="*50)

for cond in ["Depression", "Pain", "ADHD"]:
    subset = df[df["condition"] == cond]

    print(f"\n🧪 {cond}")

    print(
        subset.groupby("drugName")["rating"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )