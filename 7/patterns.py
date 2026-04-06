import re
from handlers import (
    handle_addition, handle_subtraction, handle_multiplication, handle_division, set_name
)

def register_patterns(bot):

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
        (re.compile(r"меня зовут ([а-яА-Яa-zA-Z]+)", re.IGNORECASE), set_name.__get__(bot))
    )