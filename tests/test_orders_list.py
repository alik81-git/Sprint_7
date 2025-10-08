import pytest
import requests
import allure
from config import BASE_URL


@allure.suite("Список заказов")
class TestOrdersList:

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        response = requests.get(f"{BASE_URL}/orders")
        
        assert response.status_code == 200
        
        data = response.json()
        assert "orders" in data
        assert isinstance(data["orders"], list)

    @allure.title("Получение списка заказов с лимитом")
    def test_get_orders_list_with_limit(self):
        limit = 5
        response = requests.get(f"{BASE_URL}/orders?limit={limit}")
        
        assert response.status_code == 200
        
        data = response.json()
        assert "orders" in data
        assert isinstance(data["orders"], list)
        assert len(data["orders"]) <= limit

    @allure.title("Получение списка заказов по страницам")
    def test_get_orders_list_with_page(self):
        page = 0
        response = requests.get(f"{BASE_URL}/orders?page={page}")
        
        assert response.status_code == 200
        
        data = response.json()
        assert "orders" in data
        assert isinstance(data["orders"], list)