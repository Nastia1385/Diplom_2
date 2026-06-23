import allure

from data import TestData
from methods.order_methods import OrderMethods


class TestOrder:

    @allure.step("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, create_and_delete_user, get_ingredients):
        """Тест: создание заказа авторизованным пользователем."""
        user_data = create_and_delete_user
        ingredients = get_ingredients
        response = OrderMethods.create_order(ingredients, user_data["access_token"])
        assert (response.status_code == 200
                and response.json()["success"] is True
                and "order" in response.json()
                and "number" in response.json()["order"])

    @allure.step("Создание заказа без авторизации")
    def test_create_order_without_auth(self, get_ingredients):
        """Тест: создание заказа неавторизованным пользователем."""
        ingredients = get_ingredients
        response = OrderMethods.create_order(ingredients)
        assert (response.status_code == 200
                and response.json()["success"] is True
                and "order" in response.json())

    @allure.step("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, create_and_delete_user, get_ingredients):
        """Тест: создание заказа с ингредиентами."""
        user_data = create_and_delete_user
        ingredients = get_ingredients
        response = OrderMethods.create_order(ingredients, user_data["access_token"])
        assert response.status_code == 200 and response.json()["success"] is True

    @allure.step("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, create_and_delete_user):
        """Тест: создание заказа без ингредиентов (должен вернуть ошибку)."""
        user_data = create_and_delete_user
        response = OrderMethods.create_order([], user_data["access_token"])
        assert response.status_code == 400 and response.json()["message"] == TestData.INGREDIENTS_REQUIRED_MSG

    @allure.step("Создание заказа с неверным хешем ингредиента")
    def test_create_order_invalid_hash(self, create_and_delete_user):
        """Тест: создание заказа с невалидным хешем ингредиента."""
        user_data = create_and_delete_user
        invalid_ingredients = [TestData.INVALID_INGREDIENT_HASH]
        response = OrderMethods.create_order(invalid_ingredients, user_data["access_token"])
        # Ожидаем 500 Internal Server Error
        assert response.status_code == 500
