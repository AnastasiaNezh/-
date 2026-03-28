import spacy
from datetime import datetime
from weather_api import get_weather
from state import DialogState

nlp = spacy.load("ru_core_news_sm")


def handle_greeting(self, match=None, user_data=None):
    if self.name:
        return f"Здравствуйте, {self.name}! Чем могу помочь?"
    return "Здравствуйте! Чем могу помочь?"

def handle_farewell(self, match=None, user_data=None):
    return "До свидания!"


def handle_weather(self, message_text, user_data):
    doc = nlp(message_text)
    found_city = None

    for ent in doc.ents:
        if ent.label_ in ["LOC", "GPE"]:
            found_city = ent[0].lemma_

    if user_data["state"] == DialogState.WAIT_CITY and not found_city:
        found_city = message_text.strip()

    if found_city:
        user_data["context"]["city"] = found_city

    city = user_data["context"]["city"]

    if city:
        user_data["state"] = DialogState.START
        user_data["context"]["city"] = None
        return get_weather(city)

    user_data["state"] = DialogState.WAIT_CITY
    return "В каком городе?"

def handle_addition(self, match, user_data=None):
    a = float(match.group(1))
    b = float(match.group(2))
    return f"Результат сложения: {a + b}"

def handle_subtraction(self, match, user_data=None):
    a = float(match.group(1))
    b = float(match.group(2))
    return f"Результат вычитания: {a - b}"

def handle_multiplication(self, match, user_data=None):
    a = float(match.group(1))
    b = float(match.group(2))
    return f"Результат умножения: {a * b}"

def handle_division(self, match, user_data=None):
    a = float(match.group(1))
    b = float(match.group(2))
    if b == 0:
        return "Ошибка: деление на ноль!"
    return f"Результат деления: {a / b}"

def handle_how_are_you(self, match=None, user_data=None):
    return "У меня всё отлично, спасибо!"

def handle_time(self, match=None, user_data=None):
    current_time = datetime.now().strftime("%H:%M")
    return f"Сейчас {current_time}"

def set_name(self, match, user_data=None):
    self.name = match.group(1)
    return f"Приятно познакомиться, {self.name}!"