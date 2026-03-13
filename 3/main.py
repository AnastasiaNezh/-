from bot import ChatBot
from logger import log_message, get_user

def main():
    bot = ChatBot()

    saved_name = get_user(bot.user_id)
    if saved_name:
        bot.name = saved_name
        print(f"С возвращением, {bot.name}!")

    while True:
        try:
            user_input = input("Вы: ")

            if user_input.lower() in ['выход', 'exit', 'quit']:
                print("Бот: До свидания!")
                break

            response = bot.process_message(user_input)
            log_message(user_input, response, bot.user_id, bot.name)

            print("Бот:", response)
            print()

            if response == "До свидания!":
                break

        except KeyboardInterrupt:
            print("\nБот: Программа завершена.")
            break
        except Exception as e:
            print(f"Бот: Произошла ошибка: {e}")
            print()


if __name__ == "__main__":
    main()