from datetime import datetime

def handle_greeting(self, match=None):
    if self.name:
        return f"Здравствуйте, {self.name}! Чем могу помочь?"
    return "Здравствуйте! Чем могу помочь?"

def handle_farewell(self, match=None):
    return "До свидания!"

def handle_weather(self, match):
    city = match.group(1)
    return f"Погода в городе {city}: солнечно."

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