import allure

from client.order import Order
from helpers.check_functions import CheckOrder


@allure.suite("Тесты заказа")
class TestOrder:
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        order = Order()
        ingredients = order.random_list_of_ingredients()
        response = order.create_order(ingredients)
        check_response = CheckOrder(status_code=200)
        check_response.check_status_code(response)
        check_response.assert_schema_is_valid(response.json(), check_response.body_order_schema())

    @allure.title("Создание заказа авторизованным пользователем")
    def test_create_order_with_auth(self, create_new_user):
        order = Order()
        ingredients = order.random_list_of_ingredients()
        response = order.create_order(ingredients, {"Authorization": create_new_user[2]["accessToken"]})
        check_response = CheckOrder(status_code=200)
        check_response.check_status_code(response)
        check_response.assert_schema_is_valid(response.json(), check_response.body_order_schema())

    @allure.title("Создание заказа без ингредиентов")
    def test_create_without_ingredients(self):
        order = Order()
        response = order.create_order(ingredients=[])
        check_response = CheckOrder(status_code=400, error_msg='Ingredient ids must be provided')
        check_response.check_status_code(response)
        check_response.assert_schema_is_valid(response.json(), check_response.error_shema())

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_wrong_hash_ingredients(self):
        order = Order()
        response = order.create_order(ingredients=["1", "2"])
        check_response = CheckOrder(status_code=500)
        check_response.check_status_code(response)

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_auth(self, create_new_user):
        header_auth = {"Authorization": create_new_user[2]["accessToken"]}
        order = Order()
        ingredients = order.random_list_of_ingredients()
        order.create_order(ingredients, header_auth)
        response = order.get_personal_orders(header_auth)
        check_response = CheckOrder(status_code=200)
        check_response.check_status_code(response)
        check_response.assert_schema_is_valid(response.json(), check_response.body_personal_orders_schema())

    @allure.title("Получение заказов без авторизации")
    def test_get_orders_without_auth(self, create_new_user):
        order = Order()
        response = order.get_personal_orders()
        check_response = CheckOrder(status_code=401, error_msg="You should be authorised")
        check_response.check_status_code(response)
        check_response.assert_schema_is_valid(response.json(), check_response.error_shema())
