import joblib
import spacy
from handlers import handle_weather
from patterns import register_patterns
from state import DialogState

model = joblib.load('intent_model.pkl')
nlp = spacy.load("ru_core_news_md")


def predict_with_confidence(text):
    doc = nlp(text.lower())
    vector = doc.vector.reshape(1, -1)

    probabilities = model.predict_proba(vector)
    confidence = max(probabilities[0])
    intent = model.predict(vector)[0]
    return intent, confidence

class ChatBot:
    def __init__(self):
        self.patterns = []
        self.name = None
        self.user_states = {}
        register_patterns(self)

    def get_user_data(self, user_id):
        if user_id not in self.user_states:
            self.user_states[user_id] = {
                "state": DialogState.START,
                "context": {"city": None}
            }
        return self.user_states[user_id]

    def process_message(self, message: str, user_id: int):
        original_text = message.strip()
        message_lower = original_text.lower()
        data = self.get_user_data(user_id)

        if message_lower in ["отмена", "стоп", "назад"]:
            data["state"] = DialogState.START
            data["context"]["city"] = None
            return "Диалог прерван. Чем еще я могу помочь?"

        if data["state"] == DialogState.WAIT_CITY:
            return handle_weather(self, original_text, data)

        for pattern, handler in self.patterns:
            match = pattern.search(message_lower)
            if match:
                return handler(match, data)

        intent, confidence = predict_with_confidence(original_text)

        if confidence > 0.3:
            if intent == "weather":
                return handle_weather(self, original_text, data)

            for _, handler in self.patterns:
                if intent in handler.__name__:
                    return handler(None, data)

        return "Я не понимаю запрос."