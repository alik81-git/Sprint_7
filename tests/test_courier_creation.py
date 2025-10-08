import pytest
import requests
import random
import string
import sys
import os
current_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_path)
sys.path.append(project_root)
from config import BASE_URL
from new_user import register_new_courier_and_return_login_password


class TestCourierCreation:
    BASE_URL += "/courier"

    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_missing_field(self, missing_field):
        """Тестирование создания курьера без обязательных полей"""
        payload = {
            "login": "testuser123",
            "password": "password123",
            "firstName": "Test User"
        }
        payload.pop(missing_field)
        
        response = requests.post(self.BASE_URL, data=payload)
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"


    def test_successful_courier_creation(self):
        """Тестирование успешного создания курьера"""
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for i in range(length))
            return random_string
      
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response = requests.post(self.BASE_URL, data=payload)
        assert response.status_code == 201
        assert response.json()["ok"] is True

    def test_create_courier_with_existing_login(self):
        """Тестирование создания курьера с существующим логином"""
        # Создаем первого курьера
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        # Пытаемся создать второго курьера с тем же логином
        payload = {
            "login": login,
            "password": "differentpassword",
            "firstName": "Different Name"
        }
        
        # Пытаемся создать второго курьера с таким же логином
        response = requests.post(self.BASE_URL, data=payload)
        
        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."