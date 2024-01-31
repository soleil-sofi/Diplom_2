import allure
import pytest

from client.user import User
from helpers import data_generation_functions as gen


@allure.title("Создать пользователя")
@pytest.fixture(scope="class")
def create_new_user():
    password = gen.generate_random_string()
    email = gen.generate_email()
    user = User(email=email, password=password, name=gen.generate_random_string(4))
    response_json = user.create_user().json()
    yield email, password, response_json
    user.delete_user(response_json["accessToken"])


@allure.title("Получить почту созданного пользователя (для тестов авторизации)")
@pytest.fixture(scope="function")
def email_of_existed_user(create_new_user):
    return create_new_user[0]


@allure.title("Получить пароль созданного пользователя (для тестов авторизации)")
@pytest.fixture(scope="function")
def password_of_existed_user(create_new_user):
    return create_new_user[1]
