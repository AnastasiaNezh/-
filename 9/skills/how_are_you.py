import random
from state import DialogState


def handle_how_are_you(self, message_text, user_data):
    # Если мы уже ждем ответа пользователя о его делах
    if user_data["state"] == DialogState.WAIT_USER_STATUS:
        user_data["state"] = DialogState.START
        responses = [
            "Интересно у вас!",
            "Понятно, спасибо что поделились.",
            "Ого, это звучит любопытно!",
            "Ясно, а у меня день тоже идет своим чередом."
        ]
        return random.choice(responses)

    # Если это только начало вопроса "Как дела?"
    bot_answers = [
        "У меня всё отлично, спасибо! А как ваши дела?",
        "Все системы работают в норме. Как вы себя чувствуете?",
        "Прекрасно! Радуюсь общению с вами. А у вас что нового?",
        "Я в полном порядке. А как проходит ваш день?"
    ]

    # Меняем состояние на ожидание ответа пользователя
    user_data["state"] = DialogState.WAIT_USER_STATUS
    return random.choice(bot_answers)