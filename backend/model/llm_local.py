import requests
import pandas as pd
import os

OLLAMA_URL = "http://localhost:11434/api/generate"

# =========================
# LOAD CONDITIONS FROM DATA
# =========================
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "../data/processed/final_data.csv")

data = pd.read_csv(DATA_PATH)
conditions = sorted(data["condition"].str.lower().unique())

# limit to avoid huge prompt
conditions_sample = conditions[:200]


# =========================
# CONDITION NORMALIZATION
# =========================
def normalize_condition(user_input):
    prompt = f"""
    You are a medical assistant.

    Map the user input to ONE condition from this list:

    {conditions_sample}

    Rules:
    - Return ONLY one condition from list
    - No new condition allowed
    - If unsure, choose closest match

    Input: {user_input}
    """

    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    result = response.json()["response"].strip().lower()

    # 🔥 SAFETY CHECK
    if result not in conditions:
        return find_best_match(user_input)

    return result


# =========================
# FALLBACK MATCH (SAFE)
# =========================
def find_best_match(user_input):
    user_input = user_input.lower()

    matches = [c for c in conditions if user_input in c]

    if matches:
        return matches[0]

    return conditions[0]  # fallback


# =========================
# DRUG EXPLANATION
# =========================
def explain_drug(drug, condition):
    prompt = f"""
    Explain why {drug} is used for {condition}.
    Keep it simple in 2 lines.
    """

    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    return response.json()["response"].strip()