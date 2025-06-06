import json
import pandas as pd
from collections import defaultdict

# Define clause types as per CUAD questions
CLAUSE_MAP = {
    "indemnification": "indemnity",
    "governing law": "governing_law",
    "arbitration": "arbitration",
    "termination": "termination",
    "force majeure": "force_majeure",
    "confidentiality": "confidentiality",
    "non-compete": "non_compete",
    "intellectual property": "ip",
    "change of control": "change_control",
    "limitation of liability": "limitation_liability",
    "assignment": "assignment",
    "most favored nation": "mfn",
    "non-disparagement": "non_disparagement",
}

def normalize_question(question):
    q = question.lower()
    for key in CLAUSE_MAP:
        if key in q:
            return CLAUSE_MAP[key]
    return None

def convert(json_path: str, output_csv: str):
    with open(json_path, "r") as f:
        data = json.load(f)

    rows = []
    for entry in data["data"]:
        context = entry["paragraphs"][0]["context"]
        qas = entry["paragraphs"][0]["qas"]
        labels = set()

        for qa in qas:
            if not qa["is_impossible"]:
                label = normalize_question(qa["question"])
                if label:
                    labels.add(label)

        if labels:
            row = {"text": context}
            for clause in CLAUSE_MAP.values():
                row[clause] = 1 if clause in labels else 0
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False)
    print(f"✅ Saved {len(df)} samples to {output_csv}")

if __name__ == "__main__":
    convert("data/cuad_train.json", "data/cuad_train.csv")
