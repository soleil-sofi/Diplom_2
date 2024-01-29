import requests
import allure
import random

from data_for_tests import endpoints as ep
from user import User


class Order:

    @allure.step("Получить список ингредиентов")
    def get_ingredients(self):
        return requests.get(url=ep.EP_INGREDIENTS)

    def random_list_of_ingredients(self):
        """Генерация списка из 3 существующих ингредиентов"""
        response = self.get_ingredients().json()["data"]
        ids_list = list(map(lambda d: d['_id'], response))
        result = []
        for i in range(3):
            result.append(random.choice(ids_list))
        return result

    @allure.step("Создать заказ")
    def create_order(self):
        data = {
            "ingredients": self.random_list_of_ingredients()
        }
        return requests.post(url=ep.EP_ORDERS, data=data)

    @allure.step("Получить заказ пользователя")
    def get_personal_orders(self, user: User):
        return requests.post(url=ep.EP_ORDERS, auth=user.get_access_token())
