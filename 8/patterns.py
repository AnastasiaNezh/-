import re
from skills.mathematica import (
    handle_addition, handle_subtraction,
    handle_multiplication, handle_division
)
from skills.name import set_name

def register_patterns(bot):

    bot.patterns.append(
        (re.compile(r"(\d+)\s*\+\s*(\d+)"), handle_addition)
    )

    bot.patterns.append(
        (re.compile(r"(\d+)\s*\-\s*(\d+)"), handle_subtraction)
    )

    bot.patterns.append(
        (re.compile(r"(\d+)\s*\*\s*(\d+)"), handle_multiplication)
    )

    bot.patterns.append(
        (re.compile(r"(\d+)\s*/\s*(\d+)"), handle_division)
    )

    bot.patterns.append(
        (re.compile(r"меня зовут ([а-яА-Яa-zA-Z]+)", re.IGNORECASE), set_name)
    )