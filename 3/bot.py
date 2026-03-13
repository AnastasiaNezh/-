from patterns import register_patterns

class ChatBot:
    def __init__(self):
        self.patterns = []
        self.name = None
        self.user_id = 1
        register_patterns(self)

    def process_message(self, message: str):
        original_text = message.strip()
        message_lower = original_text.lower()

        for pattern, handler in self.patterns:
            match = pattern.search(message_lower)
            if match:
                if "handle_weather" in str(handler):
                    return handler(original_text)
                return handler(match)

        return "Я не понимаю запрос."