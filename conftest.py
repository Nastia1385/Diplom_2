# import pytest
# import requests
# from faker import Faker
# from data.test_data import urls, UserData
# from helpers.api_helpers import ApiHelpers
#
# fake = Faker()
#
# @pytest.fixture
# def create_user_and_delete():
#     """Фикстура для создания уникального пользователя и удаления его после теста."""
#     user_data = {
#         "email": fake.email(),
#         "password": fake.password(),
#         "name": fake.name()
#     }
#     response = requests.post(urls.CREATE_USER, data=user_data)
#     access_token = response.json().get("accessToken")
#     yield user_data, response
#
#     # if access_token:
#     #     requests.delete(Urls.DELETE_USER, headers={"Authorization": access_token})
#
# @pytest.fixture
# def auth_token(create_user_and_delete):
#     """Фикстура для получения токена авторизации созданного пользователя."""
#     user_data, _ = create_user_and_delete
#     login_response = requests.post(urls.LOGIN, data={
#         "email": user_data["email"],
#         "password": user_data["password"]
#     })
#     token = login_response.json().get("accessToken")
#     return token
#
# @pytest.fixture
# def create_order_with_auth(auth_token):
#     """Фикстура для создания заказа авторизованным пользователем (используется в тестах)."""
#     def _create_order(ingredients=None):
#         if ingredients is None:
#             ingredients = [UserData.VALID_INGREDIENT_1, UserData.VALID_INGREDIENT_2]
#         payload = {"ingredients": ingredients}
#         response = requests.post(urls.CREATE_ORDER, json=payload, headers={"Authorization": auth_token})
#         return response
#     return _create_order

import pytest
import requests
from urls import Endpoints
from data import TestData

@pytest.fixture
def create_and_delete_user():
    """
    Фикстура для создания уникального пользователя перед тестом
    и удаления его после выполнения теста.
    """
    # Генерация уникальных данных
    import time
    unique_suffix = str(int(time.time() * 1000))
    email = f"test_{unique_suffix}@example.com"
    password = "password123"
    name = "Test User"

    user_payload = {
        "email": email,
        "password": password,
        "name": name
    }

    # Создание пользователя
    response = requests.post(Endpoints.CREATE_USER, json=user_payload)
    access_token = None
    if response.status_code == 200:
        access_token = response.json().get('accessToken')

    # Возвращаем данные для использования в тесте
    yield {
        "email": email,
        "password": password,
        "name": name,
        "access_token": access_token
    }

    # Удаление пользователя после теста, если он был создан
    if access_token:
        headers = {"Authorization": access_token}
        requests.delete(Endpoints.USER_INFO, headers=headers)

@pytest.fixture
def create_user_for_login():
    """
    Фикстура для создания пользователя, который будет существовать
    в системе для тестов логина.
    """
    import time
    unique_suffix = str(int(time.time() * 1000))
    email = f"login_test_{unique_suffix}@example.com"
    password = "password123"
    name = "Login Test User"

    user_payload = {
        "email": email,
        "password": password,
        "name": name
    }

    # Создание пользователя
    response = requests.post(Endpoints.CREATE_USER, json=user_payload)
    assert response.status_code == 200, "Не удалось создать пользователя для фикстуры login"
    access_token = response.json().get('accessToken')

    yield {
        "email": email,
        "password": password,
        "name": name,
        "access_token": access_token
    }

    # Удаление пользователя после теста
    if access_token:
        headers = {"Authorization": access_token}
        requests.delete(Endpoints.USER_INFO, headers=headers)

@pytest.fixture
def get_ingredients():
    """
    Фикстура для получения списка ингредиентов и возврата двух хешей для создания заказа.
    """
    response = requests.get(Endpoints.GET_INGREDIENTS)
    assert response.status_code == 200, "Не удалось получить ингредиенты"
    ingredients = response.json().get('data', [])
    # Берем первые два валидных ингредиента
    valid_ingredients = [item['_id'] for item in ingredients[:2]]
    return valid_ingredients