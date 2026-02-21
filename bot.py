from patterns import register_patterns
from logger import log_message


class ChatBot:
    def __init__(self):
        self.patterns = []
        self.name = None
        register_patterns(self)

    def process_message(self, message: str):
        message = message.strip().lower()

        for pattern, handler in self.patterns:
            match = pattern.search(message)
            if match:
                return handler(match)

        return "Я не понимаю запрос."


if __name__ == "__main__":
    bot = ChatBot()

    while True:
        user_input = input("Вы: ")
        response = bot.process_message(user_input)
        print("Бот:", response)
        log_message(user_input, response)

        if response == "До свидания!":
            print("Программа завершена.")
            break