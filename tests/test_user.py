import allure
import pytest

from data import TestData
from methods.user_methods import UserMethods


class TestUser:

    @allure.step("Создание уникального пользователя")
    def test_create_unique_user(self, create_and_delete_user):
        """Тест: создание уникального пользователя."""
        user_data = create_and_delete_user
        # Пользователь уже создан фикстурой, просто проверяем, что он есть
        response = UserMethods.login_user({
            "email": user_data["email"],
            "password": user_data["password"]
        })
        assert (response.status_code == 200
                and response.json()["success"] is True
                and response.json()["user"]["email"] == user_data["email"]
                and response.json()["user"]["name"] == user_data["name"])

    @allure.step("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, create_and_delete_user):
        """Тест: создание пользователя с уже существующими данными."""
        user_data = create_and_delete_user
        # Попытка создать такого же пользователя
        response = UserMethods.create_user({
            "email": user_data["email"],
            "password": user_data["password"],
            "name": user_data["name"]
        })
        assert response.status_code == 403 and response.json()["message"] == TestData.USER_ALREADY_EXISTS_MSG

    @allure.step("Создание пользователя без одного из обязательных полей")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, missing_field):
        """Тест: создание пользователя с пропущенным обязательным полем."""
        payload = {
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User"
        }
        # Удаляем одно из полей
        del payload[missing_field]
        response = UserMethods.create_user(payload)
        assert response.status_code == 403 and response.json()["message"] == TestData.REQUIRED_FIELDS_MSG

    @allure.step("Логин существующего пользователя")
    def test_login_existing_user(self, create_and_delete_user):
        """Тест: логин под существующим пользователем."""
        user_data = create_and_delete_user
        response = UserMethods.login_user({
            "email": user_data["email"],
            "password": user_data["password"]
        })
        assert (response.status_code == 200
                and response.json()["success"] is True
                and response.json()["user"]["email"] == user_data["email"]
                and response.json()["user"]["name"] == user_data["name"])

    @pytest.mark.parametrize("wrong_email, wrong_password", [
        ("wrong@example.com", "password123"),  # Неверный email
        ("test@example.com", "wrongpassword"),  # Неверный пароль
    ])
    def test_login_invalid_credentials(self, wrong_email, wrong_password):
        """Тест: логин с неверными данными."""
        # Для теста с паролем используем существующий email
        response = UserMethods.login_user({
            "email": wrong_email,
            "password": wrong_password
        })
        assert response.status_code == 401 and response.json()["message"] == TestData.INCORRECT_CREDENTIALS_MSG

    @allure.step("Изменение данных пользователя с авторизацией")
    def test_update_user_with_auth(self, create_and_delete_user):
        """Тест: изменение данных авторизованного пользователя."""
        user_data = create_and_delete_user
        new_name = "Updated User"
        new_email = f"updated_{user_data['email']}"

        payload = {"name": new_name, "email": new_email}
        response = UserMethods.update_user(payload, user_data["access_token"])

        assert (response.status_code == 200
                and response.json()["success"] is True
                and response.json()["user"]["name"] == new_name
                and response.json()["user"]["email"] == new_email)

    @allure.step("Изменение данных пользователя без авторизации")
    def test_update_user_without_auth(self, create_and_delete_user):
        """Тест: изменение данных неавторизованного пользователя (должен вернуть ошибку)."""
        new_name = "Hacked User"
        payload = {"name": new_name}
        # Не передаем токен
        response = UserMethods.update_user(payload)
        assert response.status_code == 401 and response.json()["message"] == TestData.UNAUTHORIZED_MSG
