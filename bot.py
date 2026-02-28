from patterns import register_patterns
from logger import log_message, get_user
from weather_api import get_weather
import re


class ChatBot:
    def __init__(self):
        self.patterns = []
        self.name = None
        self.user_id = 1
        register_patterns(self)
        self._register_weather_pattern()

    def _register_weather_pattern(self):
        self.patterns.append(
            (re.compile(r"погода в ([а-яА-Яa-zA-Z\-\s]+)", re.IGNORECASE), self.weather_handler)
        )

    def weather_handler(self, match):
        city = match.group(1).strip()
        return get_weather(city)

    def process_message(self, message: str):
        message = message.strip().lower()

        for pattern, handler in self.patterns:
            match = pattern.search(message)
            if match:
                return handler(match)

        return "Я не понимаю запрос."


if __name__ == "__main__":
    bot = ChatBot()

    saved_name = get_user(bot.user_id)
    if saved_name:
        bot.name = saved_name
        print(f"С возвращением, {bot.name}!")

    while True:
        user_input = input("Вы: ")
        response = bot.process_message(user_input)

        log_message(user_input, response, bot.user_id, bot.name)
        print("Бот:", response)
        print()

        if response == "До свидания!":
            print("Программа завершена.")
            break