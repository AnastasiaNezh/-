import pandas as pd
import torch
import json
import os
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

MODEL_NAME = "DeepPavlov/rubert-base-cased"
SAVE_PATH = "intent_model"

if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

# Подготовка данных
df = pd.read_csv("dataset.csv")

unique_labels = sorted(df.intent.unique())
label2id = {label: idx for idx, label in enumerate(unique_labels)}
id2label = {idx: label for label, idx in label2id.items()}

with open(f"{SAVE_PATH}/label_map.json", "w") as f:
    json.dump(id2label, f)

df["label"] = df.intent.map(label2id)

# Токенизация
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize(texts):
    return tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=64,
        return_tensors="pt"
    )

train_texts, val_texts, train_labels, val_labels = train_test_split(
    df.text.tolist(),
    df.label.tolist(),
    test_size=0.2,
    random_state=1
)

train_encodings = tokenize(train_texts)
val_encodings = tokenize(val_texts)

# Создание датасета для PyTorch
class IntentDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = IntentDataset(train_encodings, train_labels)
val_dataset = IntentDataset(val_encodings, val_labels)

# Обучение через Trainer API
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=len(unique_labels))

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=15,
    per_device_train_batch_size=8,
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    load_best_model_at_end=True
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

trainer.train()

# Сохранение модели
model.save_pretrained(SAVE_PATH)
tokenizer.save_pretrained(SAVE_PATH)
print("Обучение завершено. Модель сохранена в intent_model/")