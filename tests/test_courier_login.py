import pytest
import requests
import allure
from config import BASE_URL
from helpers import register_new_courier_and_return_login_password, login_courier, delete_courier


@allure.suite("Авторизация курьера")
class TestCourierLogin:

    @allure.title("Успешная авторизация курьера")
    def test_successful_login(self, create_and_delete_courier):
        login, password, _ = create_and_delete_courier
        
        payload = {
            "login": login,
            "password": password
        }
        
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Авторизация с неправильным паролем")
    def test_login_with_wrong_password(self, create_and_delete_courier):
        login, _, _ = create_and_delete_courier
        
        payload = {
            "login": login,
            "password": "wrongpassword"
        }
        
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]

    @allure.title("Авторизация с неправильным логином")
    def test_login_with_wrong_login(self):
        payload = {
            "login": "nonexistentuser",
            "password": "password123"
        }
        
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]

    @allure.title("Авторизация без обязательных полей")
    @pytest.mark.parametrize('missing_field', ['login'])
    def test_login_missing_field(self, missing_field):
        payload = {
            "login": "testuser",
            "password": "testpass"
        }
        payload.pop(missing_field)
        
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        
        assert response.status_code == 400
        assert "Недостаточно данных для входа" in response.json()["message"]

    @allure.title("Авторизация несуществующего пользователя")
    def test_login_nonexistent_user(self):
        payload = {
            "login": "nonexistentuser12345",
            "password": "password123"
        }
        
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]