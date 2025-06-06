from transformers import BertTokenizer, BertForSequenceClassification
import torch

LABELS = [
    "indemnity", "arbitration", "termination", "governing_law", "confidentiality",
    "force_majeure", "assignment", "ip", "change_control", "limitation_liability",
    "mfn", "non_compete", "non_disparagement"
]

# Load model + tokenizer
model_path = "/Volumes/Everything else/legal_contract_project/ml_training/bert_clause_model"

tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
model.eval()  # set to eval mode

def predict_clause_type(text: str, threshold: float = 0.5):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding="max_length")
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.sigmoid(logits)[0]

    results = []
    for i, prob in enumerate(probs):
        if prob.item() >= threshold:
            results.append(LABELS[i])

    return results or ["other"]  # default if none pass threshold
