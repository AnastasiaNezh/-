import torch
import json
import spacy
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from handlers import (
    handle_weather, handle_greeting, handle_farewell,
    handle_how_are_you, handle_time
)
from patterns import register_patterns
from state import DialogState
import torch.nn.functional as F

MODEL_PATH = "intent_model"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

nlp = spacy.load("ru_core_news_md")

with open(f"{MODEL_PATH}/label_map.json", "r") as f:
    label_map = {int(k): v for k, v in json.load(f).items()}


def predict_intent(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=64)
    with torch.no_grad():
        outputs = model(**inputs)
    probabilities = F.softmax(outputs.logits, dim=1)
    confidence, predicted_class = torch.max(probabilities, dim=1)
    intent_name = label_map.get(predicted_class.item(), "unknown")
    return intent_name, confidence.item()


class ChatBot:
    def __init__(self):
        self.patterns = []
        self.name = None
        self.user_states = {}
        register_patterns(self)

    def get_user_data(self, user_id):
        if user_id not in self.user_states:
            self.user_states[user_id] = {"state": DialogState.START, "context": {"city": None}}
        return self.user_states[user_id]

    def process_message(self, message: str, user_id: int):
        original_text = message.strip()
        message_lower = original_text.lower()
        data = self.get_user_data(user_id)

        if message_lower in ["отмена", "стоп", "назад"]:
            data["state"] = DialogState.START
            return "Диалог прерван."

        if data["state"] == DialogState.WAIT_CITY:
            return handle_weather(self, original_text, data), "weather"

        for pattern, handler in self.patterns:
            match = pattern.search(message_lower)
            if match:
                return handler(match, data), "pattern"

        intent, conf = predict_intent(original_text)
        conf_tag = f"({conf:.1%})"

        if intent == "weather":
            response = handle_weather(self, original_text, data)
        elif intent == "greeting":
            response = handle_greeting(self, None, data)
        elif intent == "farewell":
            response = handle_farewell(self, None, data)
        elif intent == "how_are_you":
            response = handle_how_are_you(self, None, data)
        elif intent == "time":
            response = handle_time(self, None, data)
        else:
            response = "Я не совсем понял, что вы имеете в виду."

            # Возвращаем ТЕКСТ и ИНТЕНТ
        return f"{response} {conf_tag}", intent