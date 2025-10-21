import random

Farewells = [
    "Было приятно пообщаться!",
    "Спасибо за беседу!",
    "До свидания!",
    "Рад был помочь!"
]

def get_farewell():
    return random.choice(Farewells)