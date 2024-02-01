import requests
import allure
import random

from data_for_tests import endpoints as ep


class Order:
    def get_ingredients(self):
        """Получить список ингредиентов"""
        return requests.get(url=ep.EP_INGREDIENTS)

    @allure.step("Создать заказ")
    def create_order(self, ingredients: list[str], headers=None):
        data = {
            "ingredients": ingredients
        }
        return requests.post(url=ep.EP_ORDERS, data=data, headers=headers)

    @allure.step("Получить заказ пользователя")
    def get_personal_orders(self, headers=None):
        return requests.get(url=ep.EP_ORDERS, headers=headers)

    @allure.step("Получить 3 случайных ингредиента")
    def random_list_of_ingredients(self):
        """Генерация списка из 3 существующих ингредиентов"""
        response = self.get_ingredients().json()["data"]
        ids_list = list(map(lambda d: d['_id'], response))
        result = []
        for i in range(3):
            result.append(random.choice(ids_list))
        return result
