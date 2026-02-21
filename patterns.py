import re
from handlers import (
    handle_greeting, handle_farewell, handle_weather,
    handle_addition, handle_subtraction, handle_multiplication, handle_division,
    handle_how_are_you, handle_time, set_name
)

def register_patterns(bot):
    bot.patterns.append(
        (re.compile(r"^(привет|здравствуй|добрый день)$", re.IGNORECASE), handle_greeting.__get__(bot))
    )

    bot.patterns.append(
        (re.compile(r"^(пока|до свидания)$", re.IGNORECASE), handle_farewell.__get__(bot))
    )

    bot.patterns.append(
        (re.compile(r"погода в ([а-яА-Яa-zA-Z\-\ ]+)", re.IGNORECASE), handle_weather.__get__(bot))
    )

    bot.patterns.append(
        (re.compile(r"(\d+)\s*\+\s*(\d+)"), handle_addition.__get__(bot))
    )

    bot.patterns.append(
        (re.compile(r"(\d+)\s*\-\s*(\d+)"), handle_subtraction.__get__(bot))
    )

    bot.patterns.append(
        (re.compile(r"(\d+)\s*\*\s*(\d+)"), handle_multiplication.__get__(bot))
    )

    bot.patterns.append(
        (re.compile(r"(\d+)\s*/\s*(\d+)"), handle_division.__get__(bot))
    )

    bot.patterns.append(
        (re.compile(r"как (у тебя )?дела", re.IGNORECASE), handle_how_are_you.__get__(bot))
    )

    bot.patterns.append(
        (re.compile(r"(сколько|какое) время", re.IGNORECASE), handle_time.__get__(bot))
    )

    bot.patterns.append(
        (re.compile(r"меня зовут ([а-яА-Яa-zA-Z]+)", re.IGNORECASE), set_name.__get__(bot))
    )