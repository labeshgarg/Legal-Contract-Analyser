import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from transformers import DataCollatorWithPadding
from datasets import Dataset as HFDataset
from torch.utils.data import Dataset
import numpy as np

# 🔧 Hyperparameters
MAX_LEN = 512
MODEL_NAME = "bert-base-uncased"
LABELS = [
    "indemnity", "arbitration", "termination", "governing_law", "confidentiality",
    "force_majeure", "assignment", "ip", "change_control", "limitation_liability",
    "mfn", "non_compete", "non_disparagement"
]

# 🧾 Load CSV
df = pd.read_csv("data/cuad_train.csv")
df["labels"] = df[LABELS].values.tolist()

# ✂️ Split
train_df, val_df = train_test_split(df, test_size=0.1, random_state=42)

# 📦 HuggingFace Dataset
train_ds = HFDataset.from_pandas(train_df)
val_ds = HFDataset.from_pandas(val_df)

# 🔠 Tokenizer
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

# 🧼 Preprocess
def preprocess(example):
    tokenized = tokenizer(example["text"], truncation=True, padding="max_length", max_length=MAX_LEN)
    tokenized["labels"] = [float(x) for x in example["labels"]]  # Leave as list[float]
    return tokenized

train_ds = train_ds.map(preprocess, remove_columns=train_ds.column_names)
val_ds = val_ds.map(preprocess, remove_columns=val_ds.column_names)

# 🧩 Torch Wrapper
class ClauseDataset(Dataset):
    def __init__(self, hf_dataset):
        self.dataset = hf_dataset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        item = self.dataset[idx]
        # Convert inputs to Long, but force labels to Float
        out = {}
        for k, v in item.items():
            if k == "labels":
                out[k] = torch.tensor(v, dtype=torch.float32)  # 🔐 This fixes it
            else:
                out[k] = torch.tensor(v, dtype=torch.long)
        return out


train_dataset = ClauseDataset(train_ds)
val_dataset = ClauseDataset(val_ds)

# 🧠 Model
model = BertForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(LABELS),
    problem_type="multi_label_classification"
)

# ⚙️ Training args
args = TrainingArguments(
    output_dir="bert_clause_model",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    logging_steps=10,
    save_total_limit=2,
    load_best_model_at_end=True,
)

# 📈 Metrics
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = (logits > 0.5).astype(int)
    acc = (preds == labels).mean()
    return {"accuracy": acc}

# 🧯 Trainer
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
    data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
    compute_metrics=compute_metrics
)

# 🚀 Train
trainer.train()

# 💾 Save
model.save_pretrained("bert_clause_model")
tokenizer.save_pretrained("bert_clause_model")
