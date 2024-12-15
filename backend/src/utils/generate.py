from random import randint
from uuid import uuid4
import string
import random


def generate_random_code():
    return randint(100000, 999999)


def generate_uuid():
    return uuid4()


def generate_random_password(length=12):
    """
    Генерирует случайный пароль для пользователя.

    :param length: Длина пароля (по умолчанию 12 символов).
    :return: Случайный пароль.
    """
    # Определяем набор символов для пароля
    characters = string.ascii_letters + string.digits

    # Генерируем случайный пароль
    password = ''.join(random.choice(characters) for i in range(length))
    return password