from datetime import datetime

def handle_time(self, match=None, user_data=None):
    current_time = datetime.now().strftime("%H:%M")
    return f"Сейчас {current_time}"