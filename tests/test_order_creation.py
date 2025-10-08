import pytest
import requests
import sys
import os
current_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_path)
sys.path.append(project_root)
from config import BASE_URL


class TestOrderCreation:
    BASE_URL += "/orders"
    
    @pytest.mark.parametrize('color', [
        ["BLACK"],
        ["GREY"], 
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_different_colors(self, color):
        """Тестирование создания заказа с разными цветами"""
        payload = {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "ул. Пушкина, д. 1",
            "metroStation": 4,
            "phone": "+79991234567",
            "rentTime": 5,
            "deliveryDate": "2024-12-31",
            "comment": "Тестовый заказ",
            "color": color
        }
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 201
        assert "track" in response.json()
        
        track_number = response.json()["track"]
        assert isinstance(track_number, int)
        assert track_number > 0

    def test_create_order_without_color(self):
        """Тестирование создания заказа без указания цвета"""
        payload = {
            "firstName": "Петр",
            "lastName": "Петров",
            "address": "ул. Лермонтова, д. 10",
            "metroStation": 5,
            "phone": "+79997654321",
            "rentTime": 3,
            "deliveryDate": "2024-11-30",
            "comment": "Второй тестовый заказ"
        }
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 201
        assert "track" in response.json()

    def test_create_order_minimal_data(self):
        """Тестирование создания заказа с минимальными данными"""
        payload = {
            "firstName": "Минимал",
            "lastName": "Тестов",
            "address": "Минимальный адрес",
            "metroStation": 1,
            "phone": "+79991112233",
            "rentTime": 1,
            "deliveryDate": "2024-10-01"
        }
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 201
        assert "track" in response.json()