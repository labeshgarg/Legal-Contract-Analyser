import random

# Simple keyword-based heuristic for risk scores
KEYWORD_RISK_MAP = {
    "indemnify": 90,
    "liability": 80,
    "terminate": 70,
    "penalty": 85,
    "arbitration": 30,
    "force majeure": 40,
    "governing law": 20,
    "confidential": 20,
}


def calculate_risk_score(clause_text: str) -> int:
    text = clause_text.lower()
    score = 10  # base risk

    for keyword, risk in KEYWORD_RISK_MAP.items():
        if keyword in text:
            score = max(score, risk)

    # Add small noise to simulate variation
    score += random.randint(-5, 5)
    return max(0, min(score, 100))
