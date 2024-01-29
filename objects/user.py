import requests
import allure

from data_for_tests import endpoints as ep


class User:

    def __init__(self, login, password, name):
        self.email = login
        self.password = password
        self.name = name
        self.__access_token = None
        self.__refresh_token = None

    @allure.step("Создать пользователя")
    def create_user(self):
        data = {
            "email": self.email,
            "password": self.password,
            "name": self.name
        }
        return requests.post(url=ep.EP_REGISTER, data=data)

    @allure.step("Залогиниться под пользователем {self.login}")
    def login_user(self):
        data = {
            "email": self.email,
            "password": self.password
        }
        response = requests.post(url=ep.EP_REGISTER, data=data)
        self.__access_token = response.json()["accessToken"]
        self.__refresh_token = response.json()["refreshToken"]
        return response

    @allure.step("Изменить данные пользователя {self.login}")
    def update_user(self):
        return requests.post(url=ep.EP_USER, auth=self.__access_token)

    @allure.step("Удалить пользователя {self.login}")
    def delete_user(self):
        return requests.delete(url=ep.EP_USER, auth=self.__access_token)
