def handle_greeting(self, match=None, user_data=None):
    if self.name:
        return f"Здравствуйте, {self.name}! Чем могу помочь?"
    return "Здравствуйте! Чем могу помочь?"