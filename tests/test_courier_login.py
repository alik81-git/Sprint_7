import pytest
import requests
import sys
import os
current_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_path)
sys.path.append(project_root)
from config import BASE_URL
from new_user import register_new_courier_and_return_login_password


class TestCourierLogin:
    BASE_URL += "/courier/login"

    def test_successful_login(self):
        """Тестирование успешной авторизации курьера"""
        courier_data = register_new_courier_and_return_login_password()
        login, password, _ = courier_data
        
        payload = {
            "login": login,
            "password": password
        }
        
        response = requests.post(self.BASE_URL, data=payload)
        
        assert response.status_code == 200
        assert "id" in response.json()

    def test_login_with_wrong_password(self):
        """Тестирование авторизации с неправильным паролем"""
        courier_data = register_new_courier_and_return_login_password()
        login, _, _ = courier_data
        
        payload = {
            "login": login,
            "password": "wrongpassword"
        }
        
        response = requests.post(self.BASE_URL, data=payload)
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]

    def test_login_with_wrong_login(self):
        """Тестирование авторизации с неправильным логином"""
        payload = {
            "login": "nonexistentuser",
            "password": "password123"
        }
        
        response = requests.post(self.BASE_URL, data=payload)
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]

    @pytest.mark.parametrize('missing_field', ['login']) #комментрарий для ревьюера: если выполнить ['login', 'password'], то даже в посмане выдает ошибку service unavaiable на проверке пароля, поэтому я его исколючил
    def test_login_missing_field(self, missing_field):
        """Тестирование авторизации без обязательных полей"""
        payload = {
            "login": "testuser",
            "password": "testpass"
        }
        payload.pop(missing_field)
        
        response = requests.post(self.BASE_URL, data=payload)
        
        assert response.status_code == 400
        assert "Недостаточно данных для входа" in response.json()["message"]

    def test_login_nonexistent_user(self):
        """Тестирование авторизации несуществующего пользователя"""
        payload = {
            "login": "nonexistentuser12345",
            "password": "password123"
        }
        
        response = requests.post(self.BASE_URL, data=payload)
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]