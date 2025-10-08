import pytest
import requests
import allure
from config import BASE_URL
from helpers import generate_random_string, register_new_courier_and_return_login_password


@allure.suite("Создание курьера")
class TestCourierCreation:

    @allure.title("Создание курьера без обязательных полей")
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_missing_field(self, missing_field):
        payload = {
            "login": "testuser123",
            "password": "password123",
            "firstName": "Test User"
        }
        payload.pop(missing_field)
        
        response = requests.post(f"{BASE_URL}/courier", data=payload)
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Успешное создание курьера")
    def test_successful_courier_creation(self, create_and_delete_courier):
        login, password, first_name = create_and_delete_courier
        
        # Проверяем, что курьер был создан (фикстура уже создала его)
        courier_login_response = requests.post(
            f"{BASE_URL}/courier/login", 
            data={"login": login, "password": password}
        )
        
        assert courier_login_response.status_code == 200
        assert "id" in courier_login_response.json()

    @allure.title("Создание курьера с существующим логином")
    def test_create_courier_with_existing_login(self, create_and_delete_courier):
        login, password, first_name = create_and_delete_courier
        
        payload = {
            "login": login,
            "password": "differentpassword",
            "firstName": "Different Name"
        }
        
        response = requests.post(f"{BASE_URL}/courier", data=payload)
        
        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."