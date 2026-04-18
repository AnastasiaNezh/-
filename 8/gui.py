import os
from datetime import datetime

os.environ['TCL_LIBRARY'] = r'C:\Users\Анастасия\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Анастасия\AppData\Local\Programs\Python\Python313\tcl\tk8.6'

import customtkinter as ctk
from bot import ChatBot
from logger import get_user, get_chat_history, log_message, clear_chat_history

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BOT_COLOR = ("#E0F7FA", "#006064")
USER_COLOR = ("#81D4FA", "#01579B")
TEXT_COLOR = ("#000000", "#FFFFFF")


class ChatGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.bot = ChatBot()
        self.user_id = 1
        self.title("Алёнушка bot")
        self.geometry("500x700")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.chat_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.chat_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)

        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.user_input = ctk.CTkEntry(self.input_frame, placeholder_text="Введите сообщение...")
        self.user_input.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.user_input.bind("<Return>", lambda e: self.send_message())


        self.send_button = ctk.CTkButton(self.input_frame, text="Отправить", width=80,
                                         command=self.send_message)
        self.send_button.grid(row=0, column=1)

        self.message_row = 0
        self.last_displayed_date = None
        self.load_welcome_message()


    def add_date_separator(self, date_str):
        date_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        date_container.grid(row=self.message_row, column=0, pady=15, sticky="ew")

        date_bubble = ctk.CTkFrame(
            date_container,
            fg_color=("#E0E0E0", "#2B2B2B"),
            corner_radius=10
        )
        date_bubble.pack(expand=True)

        date_label = ctk.CTkLabel(
            date_bubble,
            text=date_str,
            font=("Arial", 11, "bold"),
            text_color=("gray20", "gray80")
        )
        date_label.pack(padx=12, pady=4)

        self.message_row += 1

    def load_welcome_message(self):
        history = get_chat_history(self.user_id)
        for user_msg, bot_res, ts in history:
            # Просто выводим текстовые пузыри из истории
            self.add_message_bubble("Вы", user_msg, is_user=True, full_date_str=ts)
            self.add_message_bubble("Алёнушка", bot_res, is_user=False, full_date_str=ts)

        saved_name = get_user(self.user_id)
        if saved_name:
            self.bot.name = saved_name
            self.add_message_bubble("Алёнушка", f"С возвращением, {self.bot.name}!", is_user=False)
        else:
            self.add_message_bubble("Алёнушка", "Привет! Как я могу к вам обращаться?", is_user=False)
    def add_message_bubble(self, sender, text, is_user, full_date_str=None):
        if full_date_str:
            dt_obj = datetime.strptime(full_date_str, "%Y-%m-%d %H:%M:%S")
            current_date = dt_obj.strftime("%d.%m.%Y")
            display_time = dt_obj.strftime("%H:%M")
        else:
            now = datetime.now()
            current_date = now.strftime("%d.%m.%Y")
            display_time = now.strftime("%H:%M")

        if current_date != self.last_displayed_date:
            self.add_date_separator(current_date)
            self.last_displayed_date = current_date

        bubble_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        side = "e" if is_user else "w"
        color = USER_COLOR if is_user else BOT_COLOR

        bubble_container.grid(row=self.message_row, column=0, pady=5, padx=10, sticky=side)
        self.message_row += 1

        bubble = ctk.CTkFrame(bubble_container, fg_color=color, corner_radius=15)
        bubble.pack(side="top", anchor=side)

        message_label = ctk.CTkLabel(
            bubble, text=text, text_color=TEXT_COLOR,
            font=("Arial", 14), wraplength=300, justify="left"
        )
        message_label.pack(padx=15, pady=(10, 5))

        info_text = f"{sender} • {display_time}"
        info_label = ctk.CTkLabel(bubble_container, text=info_text, font=("Arial", 10), text_color="gray")
        info_label.pack(side="top", anchor=side, padx=5, pady=(2, 0))

        self.after(10, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        self.chat_frame.update_idletasks()
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def send_message(self):
        text = self.user_input.get().strip()
        if not text:
            return

        self.add_message_bubble("Вы", text, is_user=True)
        self.user_input.delete(0, "end")

        self.after(500, self.get_bot_response, text)

    def clear_ui_chat(self):
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self.message_row = 0
        self.last_displayed_date = None

    def get_bot_response(self, text):
        if text.lower() == "удалить историю":
            clear_chat_history(self.user_id)
            self.clear_ui_chat()
            self.add_message_bubble("Система", "История переписки успешно удалена.", is_user=False)
            return

        try:
            response, intent = self.bot.process_message(text, self.user_id)
            self.finish_bot_response(response, intent, text)
        except Exception as e:
            self.add_message_bubble("Система", f"Ошибка: {e}", is_user=False)

    def finish_bot_response(self, response, intent, original_text):
        self.add_message_bubble("Алёнушка", response, is_user=False)
        log_message(original_text, response, self.user_id, self.bot.name)

        if intent == "farewell":
            self.after(2000, self.destroy)

if __name__ == "__main__":
    app = ChatGUI()
    app.mainloop()