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