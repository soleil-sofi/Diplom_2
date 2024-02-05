import random
import string


def generate_random_string(length=10):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string


def generate_email():
    login = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
    domain = random.choice(['ya.ru', 'yandex.ru', 'mail.ru', 'gmail.com'])

    email = login + '@' + domain
    return email
