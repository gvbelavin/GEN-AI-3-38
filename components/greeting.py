import random

Greetings = [
    "Здравствуйте!",
    "Приветствую!",
    "Добрый день!",
    "Рад вас видеть!"
]

def get_greeting():
    """Выбирает случайное приветствие"""
    return random.choice(Greetings)

if __name__ == "__main__":
    print("Тест для приветствий:")
    for i in range(3):
        print(f"{i+1}. {get_greeting()}")