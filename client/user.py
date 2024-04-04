import requests
import allure

from data_for_tests import endpoints as ep


class User:

    def __init__(self, email, password=None, name=None):
        self.email = email
        self.password = password
        self.name = name

    @allure.step("Создать пользователя")
    def create_user(self):
        data = {
            "email": self.email,
            "password": self.password,
            "name": self.name
        }
        return requests.post(url=ep.EP_REGISTER, data=data)

    @allure.step("Залогиниться под пользователем")
    def login_user(self):
        data = {
            "email": self.email,
            "password": self.password
        }
        response = requests.post(url=ep.EP_LOGIN, data=data)
        return response

    @allure.step("Изменить данные пользователя")
    def update_user(self, auth=None):
        data = {
            "email": self.email,
            "name": self.name
        }
        return requests.patch(url=ep.EP_USER, data=data, headers={"Authorization": auth})

    @allure.step("Удалить пользователя")
    def delete_user(self, auth):
        return requests.delete(url=ep.EP_USER, headers={"Authorization": auth})
