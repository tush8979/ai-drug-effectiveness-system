from predict import rank_drugs

tests = ["Depression", "Pain", "ADHD", "High Blood Pressure"]

for cond in tests:
    print(f"\n🧪 {cond}")

    results = rank_drugs(cond, 30, 24, 5)

    for i, r in enumerate(results[:5]):
        print(f"{i+1}. {r['drug']} → {r['score']}")