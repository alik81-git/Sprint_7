# conftest.py
import pytest
import requests
import allure
from helpers import register_new_courier_and_return_login_password, delete_courier, login_courier
from config import BASE_URL


@pytest.fixture
def create_and_delete_courier():
    """Фикстура для создания и последующего удаления курьера"""
    courier_data = register_new_courier_and_return_login_password()
    login, password, first_name = courier_data
    
    yield login, password, first_name
    
    # Пост-условие: удаление курьера
    courier_id = login_courier(login, password)
    if courier_id:
        delete_courier(courier_id)


@pytest.fixture
def create_order():
    """Фикстура для создания заказа"""
    def _create_order(color=None):
        payload = {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "ул. Пушкина, д. 1",
            "metroStation": 4,
            "phone": "+79991234567",
            "rentTime": 5,
            "deliveryDate": "2024-12-31",
            "comment": "Тестовый заказ"
        }
        
        if color is not None:
            payload["color"] = color
            
        response = requests.post(f"{BASE_URL}/orders", json=payload)
        return response.json().get("track")
    
    return _create_order