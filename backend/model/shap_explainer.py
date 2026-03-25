import shap
import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "models")

model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
columns = joblib.load(os.path.join(MODEL_DIR, "columns.pkl"))

explainer = shap.Explainer(model)

def explain_prediction(input_dict):
    df = pd.DataFrame([input_dict])
    df = pd.get_dummies(df)
    df = df.reindex(columns=columns, fill_value=0)

    scaled = scaler.transform(df)
    shap_values = explainer(scaled)

    feature_importance = {}

    for i, col in enumerate(columns):
        val = float(shap_values.values[0][i])

        # ✅ FILTER ONLY IMPORTANT FEATURES
        if abs(val) > 0.1:

            # clean feature names
            if col.startswith("drugName_"):
                name = col.replace("drugName_", "")
            elif col.startswith("condition_"):
                continue  # ❌ REMOVE unrelated conditions
            else:
                name = col

            feature_importance[name] = val

    # sort
    feature_importance = dict(
        sorted(feature_importance.items(), key=lambda x: abs(x[1]), reverse=True)
    )

    return feature_importance