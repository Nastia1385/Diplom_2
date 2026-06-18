import requests
from urls import Endpoints

class UserMethods:
    """Класс для работы с методами пользователя."""

    @staticmethod
    def create_user(payload):
        """Создание пользователя."""
        return requests.post(Endpoints.CREATE_USER, json=payload)

    @staticmethod
    def login_user(payload):
        """Авторизация пользователя."""
        return requests.post(Endpoints.LOGIN_USER, json=payload)

    @staticmethod
    def update_user(payload, access_token=None):
        """Обновление данных пользователя."""
        headers = {}
        if access_token:
            headers["Authorization"] = access_token
        return requests.patch(Endpoints.USER_INFO, json=payload, headers=headers)

    @staticmethod
    def get_user_info(access_token):
        """Получение данных пользователя."""
        headers = {"Authorization": access_token}
        return requests.get(Endpoints.USER_INFO, headers=headers)

    @staticmethod
    def delete_user(access_token):
        """Удаление пользователя."""
        headers = {"Authorization": access_token}
        return requests.delete(Endpoints.USER_INFO, headers=headers)