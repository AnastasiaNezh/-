from datetime import datetime

def log_message(user, bot):
    with open("chat_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] USER: {user}\n")
        f.write(f"[{datetime.now()}] BOT: {bot}\n")