from bot_core import ChatBot


def main():
    bot = ChatBot()


    while True:
        try:
            user_input = input("Вы: ")

            if user_input.lower() in ['выход', 'exit', 'quit']:
                print("Бот: До свидания!")
                break

            response = bot.process(user_input)
            print("Бот:", response)
            print()

        except KeyboardInterrupt:
            print("\nБот: Программа завершена.")
            break
        except Exception as e:
            print(f"Бот: Произошла ошибка: {e}")
            print()


if __name__ == "__main__":
    main()