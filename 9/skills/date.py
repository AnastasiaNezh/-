from datetime import datetime

def handle_date(self, message=None, user_data=None):
    now = datetime.now()
    months = ["января", "февраля", "марта", "апреля", "мая", "июня",
              "июля", "августа", "сентября", "октября", "ноября", "декабря"]
    day = now.day
    month = months[now.month - 1]
    year = now.year
    return f"Сегодня {day} {month} {year} года."