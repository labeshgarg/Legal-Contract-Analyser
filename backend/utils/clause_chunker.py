import re
from typing import List, Dict

# Simple list of clause types with indicative keywords (can expand later)
CLAUSE_TYPES = {
    "indemnity": ["indemnify", "liability", "compensate"],
    "arbitration": ["arbitration", "dispute resolution", "tribunal"],
    "force majeure": ["force majeure", "acts of god", "beyond control"],
    "termination": ["terminate", "termination", "expiry"],
    "confidentiality": ["confidential", "nondisclosure", "privacy"],
    "governing law": ["governing law", "jurisdiction", "venue"],
}


def split_into_clauses(text: str) -> List[str]:
    # Heuristic: split on large breaks / numbered sections / ALL CAPS titles
    pattern = r"(?=\n\s*\d+[\.\)]|\n\s*[A-Z\s]{5,}\n|\n\n)"
    clauses = re.split(pattern, text)
    clauses = [c.strip() for c in clauses if len(c.strip()) > 40]
    return clauses


def classify_clause(clause: str) -> str:
    clause_lower = clause.lower()
    for label, keywords in CLAUSE_TYPES.items():
        if any(keyword in clause_lower for keyword in keywords):
            return label
    return "other"
