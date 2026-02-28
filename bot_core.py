import re
from weather_api import get_weather


class ChatBot:
    def __init__(self):
        self.patterns = []
        self._register_patterns()

    def _register_patterns(self):
        self.patterns.append(
            (re.compile(r"привет|здравствуй|добрый день", re.IGNORECASE), self.greet)
        )

        self.patterns.append(
            (re.compile(r"погода в ([а-яА-Яa-zA-Z\-\s]+)", re.IGNORECASE), self.weather)
        )

    def greet(self, match):
        return "Здравствуйте! Чем могу помочь?"

    def weather(self, match):
        city = match.group(1).strip()
        return get_weather(city)

    def process(self, message):
        message = message.strip().lower()

        for pattern, handler in self.patterns:
            match = pattern.search(message)
            if match:
                return handler(match)

        return "Не понимаю запрос. Попробуйте спросить о погоде или поздороваться."