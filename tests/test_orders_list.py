import pytest
import requests
import sys
import os
current_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_path)
sys.path.append(project_root)
from config import BASE_URL


class TestOrdersList:
    BASE_URL += "/orders"

    def test_get_orders_list(self):
        """Тестирование получения списка заказов"""
        response = requests.get(self.BASE_URL)
        
        assert response.status_code == 200
        
        data = response.json()
        
        # Проверяем структуру ответа
        assert "orders" in data
        assert isinstance(data["orders"], list)
        

    def test_get_orders_list_with_limit(self):
        """Тестирование получения списка заказов с лимитом"""
        limit = 5
        response = requests.get(f"{self.BASE_URL}?limit={limit}")
        
        assert response.status_code == 200
        
        data = response.json()
        assert "orders" in data
        assert isinstance(data["orders"], list)
        
        # Проверяем, что количество заказов не превышает лимит
        assert len(data["orders"]) <= limit

    def test_get_orders_list_with_page(self):
        """Тестирование получения списка заказов по страницам"""
        page = 0
        response = requests.get(f"{self.BASE_URL}?page={page}")
        
        assert response.status_code == 200
        
        data = response.json()
        assert "orders" in data
        assert isinstance(data["orders"], list)