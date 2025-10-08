# helpers.py
import random
import string
import requests
from config import BASE_URL


def generate_random_string(length):
    """Генерация случайной строки из букв нижнего регистра"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def register_new_courier_and_return_login_password():
    """Регистрация нового курьера и возврат логина, пароля и имени"""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f"{BASE_URL}/courier", data=payload)

    if response.status_code == 201:
        return login, password, first_name
    return None, None, None


def delete_courier(courier_id):
    """Удаление курьера по ID"""
    response = requests.delete(f"{BASE_URL}/courier/{courier_id}")
    return response.status_code == 200


def login_courier(login, password):
    """Авторизация курьера и получение ID"""
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/courier/login", data=payload)
    if response.status_code == 200:
        return response.json().get("id")
    return None