import allure
import pytest
from pytest_lazyfixture import lazy_fixture

from client.user import User
from helpers.check_functions import CheckUser
from helpers import data_generation_functions as gen


class TestUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self):
        email = gen.generate_email()
        password = gen.generate_random_string()
        name = gen.generate_random_string(4)
        user = User(email, password, name)
        response = user.create_user()
        check_response = CheckUser(status_code=200, email=email, name=name)
        check_response.check_status_code(response)
        check_response.assert_schema_is_valid(response.json(), check_response.body_user_schema())

        user.delete_user(response.json()["accessToken"])

    @allure.title("Создание неуникального пользователя")
    def test_create_nonunique_user(self, create_new_user):
        user = User(create_new_user[0], gen.generate_random_string(), create_new_user[2]["user"]["name"])
        response = user.create_user()
        check_response = CheckUser(status_code=403, error_msg="User already exists")
        check_response.check_status_code(response)
        check_response.assert_schema_is_valid(response.json(), check_response.error_shema())

    @allure.title("Создание пользователя без обязательных полей")
    @pytest.mark.parametrize("email, password, name", [[None, gen.generate_email(), gen.generate_random_string(4)],
                                                       [gen.generate_email(), None, gen.generate_random_string(4)],
                                                       [gen.generate_email(), gen.generate_random_string(), None]],
                             ids=["Empty email", "Empty password", "Empty name"])
    def test_create_user_with_empty_fields(self, email, password, name):
        user = User(email, password, name)
        response = user.create_user()
        check_response = CheckUser(status_code=403, error_msg="Email, password and name are required fields")
        check_response.check_status_code(response)
        check_response.assert_schema_is_valid(response.json(), check_response.error_shema())

    @allure.title("Логин существующего пользователя")
    def test_login_existed_user(self, create_new_user):
        name = create_new_user[2]["user"]["name"]
        user = User(email=create_new_user[0], password=create_new_user[1], name=name)
        response = user.login_user()
        print(response.json())
        check_response = CheckUser(status_code=200, email=create_new_user[0], name=name)
        check_response.check_status_code(response)
        check_response.assert_schema_is_valid(response.json(), check_response.body_user_schema())

    @allure.title("Логин пользователя с некорректной почтой/паролем")
    @pytest.mark.parametrize("email, password", [(lazy_fixture('email_of_existed_user'), gen.generate_random_string()),
                                                 (gen.generate_email(), lazy_fixture('password_of_existed_user')),
                                                 (gen.generate_email(), gen.generate_random_string())],
                             ids=["Wrong password", "Wrong email", "Wrong email and password"])
    def test_login_wrong_log_or_pass(self, email, password):
        user = User(email, password)
        response = user.login_user()
        check_response = CheckUser(status_code=401, error_msg='email or password are incorrect')
        check_response.check_status_code(response)
        check_response.assert_schema_is_valid(response.json(), check_response.error_shema())

    @allure.title("Редактирование авторизованного пользователя")
    def test_update_user(self, create_new_user):
        name = gen.generate_random_string()
        user = User(email=create_new_user[0], name=name)
        response = user.update_user(create_new_user[2]["accessToken"])
        check_response = CheckUser(status_code=200, email=create_new_user[0], name=name)
        check_response.check_status_code(response)
        check_response.assert_schema_is_valid(response.json(), check_response.body_user_schema())

    @allure.title("Редактирование неавторизованного пользователя")
    def test_update_user_without_auth(self, create_new_user):
        email = gen.generate_email()
        user = User(email=email)
        response = user.update_user()
        check_response = CheckUser(status_code=401, error_msg='You should be authorised')
        check_response.check_status_code(response)
        check_response.assert_schema_is_valid(response.json(), check_response.error_shema())
