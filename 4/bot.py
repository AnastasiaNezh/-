from patterns import register_patterns
from state import DialogState

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
            return self.patterns[0][1](original_text, data)

        for pattern, handler in self.patterns:
            match = pattern.search(message_lower)
            if match:
                if "handle_weather" in handler.__name__:
                    return handler(original_text, data)

                try:
                    return handler(match, data)
                except TypeError:
                    return handler(match)

        return "Я не понимаю запрос."