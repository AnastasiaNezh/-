import torch
import json
import spacy
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from skills.weather import handle_weather
from skills.time import handle_time
from skills.greeting import handle_greeting
from skills.farewell import handle_farewell
from skills.how_are_you import handle_how_are_you
from skills.date import handle_date
from skills.help import handle_help
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
        self.skills = {
            "weather": handle_weather,
            "greeting": handle_greeting,
            "farewell": handle_farewell,
            "how_are_you": handle_how_are_you,
            "time": handle_time,
            "date": handle_date,
            "help": handle_help
        }

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

        if data["state"] == DialogState.WAIT_USER_STATUS:
            return handle_how_are_you(self, original_text, data), "how_are_you"

        for pattern, handler in self.patterns:
            match = pattern.search(message_lower)
            if match:
                return handler(self, match, data), "pattern"

        intent, conf = predict_intent(original_text)
        skill_handler = self.skills.get(intent)

        if skill_handler:
            response = skill_handler(self, original_text, data)
            return f"{response} ({conf:.1%})", intent

        return "Извините, я не понял ваш запрос.", "unknown"