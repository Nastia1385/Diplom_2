import allure

from data import TestData
from methods.order_methods import OrderMethods


@allure.epic("Тесты получения заказов пользователя")
class TestUserOrders:

    @allure.step("Получение заказов авторизованного пользователя")
    def test_get_orders_with_auth(self, create_and_delete_user, get_ingredients):
        """Тест: получение заказов авторизованным пользователем."""
        user_data = create_and_delete_user
        ingredients = get_ingredients
        # Сначала создаем заказ, чтобы он был в списке
        OrderMethods.create_order(ingredients, user_data["access_token"])
        # Получаем заказы
        response = OrderMethods.get_user_orders(user_data["access_token"])
        assert response.status_code == 200 and response.json()["success"] is True
        # Проверяем, что заказ есть в списке
        assert "orders" in response.json() and len(response.json()["orders"]) > 0

    @allure.step("Получение заказов неавторизованного пользователя")
    def test_get_orders_without_auth(self):
        """Тест: получение заказов неавторизованным пользователем."""
        response = OrderMethods.get_user_orders()
        assert response.status_code == 401 and response.json()["message"] == TestData.UNAUTHORIZED_MSG
