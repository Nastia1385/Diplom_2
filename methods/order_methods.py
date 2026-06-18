import requests
from urls import Endpoints

class OrderMethods:
    """Класс для работы с методами заказов."""

    @staticmethod
    def create_order(ingredients, access_token=None):
        """Создание заказа."""
        payload = {"ingredients": ingredients}
        headers = {}
        if access_token:
            headers["Authorization"] = access_token
        return requests.post(Endpoints.CREATE_ORDER, json=payload, headers=headers)

    @staticmethod
    def get_user_orders(access_token=None):
        """Получение заказов конкретного пользователя."""
        headers = {}
        if access_token:
            headers["Authorization"] = access_token
        return requests.get(Endpoints.GET_USER_ORDERS, headers=headers)