import spacy
from datetime import datetime
from weather_api import get_weather

nlp = spacy.load("ru_core_news_sm")

def handle_greeting(self, match=None):
    if self.name:
        return f"Здравствуйте, {self.name}! Чем могу помочь?"
    return "Здравствуйте! Чем могу помочь?"

def handle_farewell(self, match=None):
    return "До свидания!"


def handle_weather(self, message_text):
    doc = nlp(message_text)

    city = None
    date_text = None

    for ent in doc.ents:
        if ent.label_ in ["LOC", "GPE"]:
            city = ent[0].lemma_
        elif ent.label_ == "DATE":
            date_text = ent.text

    lemmas = [token.lemma_.lower() for token in doc]

    if "погода" in [token.lemma_.lower() for token in doc]:
        if city:
            weather_report = get_weather(city)
            if date_text:
                return f"{weather_report}\n(Запрос обработан на дату: {date_text})"
            return weather_report
        else:
            return "Я понял, что вас интересует погода, но не нашел название города в запросе."

    return "Не совсем понял ваш запрос."

def handle_addition(self, match):
    a = float(match.group(1))
    b = float(match.group(2))
    return f"Результат сложения: {a + b}"

def handle_subtraction(self, match):
    a = float(match.group(1))
    b = float(match.group(2))
    return f"Результат вычитания: {a - b}"

def handle_multiplication(self, match):
    a = float(match.group(1))
    b = float(match.group(2))
    return f"Результат умножения: {a * b}"

def handle_division(self, match):
    a = float(match.group(1))
    b = float(match.group(2))
    if b == 0:
        return "Ошибка: деление на ноль!"
    return f"Результат деления: {a / b}"

def handle_how_are_you(self, match=None):
    return "У меня всё отлично, спасибо!"

def handle_time(self, match=None):
    current_time = datetime.now().strftime("%H:%M")
    return f"Сейчас {current_time}"

def set_name(self, match):
    self.name = match.group(1)
    return f"Приятно познакомиться, {self.name}!"