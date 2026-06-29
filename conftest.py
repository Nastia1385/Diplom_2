import time

import pytest
import requests

from urls import Endpoints


@pytest.fixture
def create_and_delete_user():
    """
    Фикстура для создания уникального пользователя перед тестом
    и удаления его после выполнения теста.
    """
    # Генерация уникальных данных
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
    ingredients = response.json().get('data', [])
    # Берем первые два валидных ингредиента
    valid_ingredients = [item['_id'] for item in ingredients[:2]]
    return valid_ingredients


@pytest.fixture
def unique_user_data():
    """
    Фикстура для генерации уникальных данных пользователя.
    После выполнения теста выполняет очистку - удаляет созданного пользователя.
    """
    # 1. Генерация уникальных данных
    unique_suffix = str(int(time.time() * 1000))
    email = f"test_{unique_suffix}@example.com"
    password = "password123"
    name = "Test User"

    user_payload = {
        "email": email,
        "password": password,
        "name": name
    }

    # Возвращаем данные для использования в тесте
    yield user_payload

    # 2. Очистка после теста - удаление пользователя
    # Пытаемся получить токен для удаления
    login_response = requests.post(Endpoints.LOGIN_USER, json={
        "email": email,
        "password": password
    })

    if login_response.status_code == 200:
        access_token = login_response.json().get('accessToken')
        if access_token:
            headers = {"Authorization": access_token}
            requests.delete(Endpoints.USER_INFO, headers=headers)
