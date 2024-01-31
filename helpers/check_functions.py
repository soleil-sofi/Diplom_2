from requests import Response
from jsonschema import validate


class BaseCheck:
    def __init__(self, status_code: int = None, error_msg: str = None):
        self.status_code = status_code
        self.error_msg = error_msg

    def check_status_code(self, response: Response):
        assert response.status_code == self.status_code

    @staticmethod
    def assert_schema_is_valid(response: dict, schema: dict) -> None:
        """Проверка, что значения в JSON ответе валидные"""
        validate(instance=response, schema=schema)

    def error_shema(self):
        return {
            "type": "object",
            "required": [
                "success",
                "message"
            ],
            "properties": {
                "success": {"type": "boolean", "const": False},
                "message": {"type": "string", "const": self.error_msg}
            }
        }


class CheckUser(BaseCheck):
    def __init__(self, status_code: int = None, error_msg: str = None, email: str = None, name: str = None):
        BaseCheck.__init__(self, status_code, error_msg)
        self.email = email
        self.name = name

    def body_user_schema(self):
        return {
            "type": "object",
            "required": [
                "success",
                "user"
            ],
            "properties": {
                "success": {"type": "boolean", "const": True},
                "accessToken": {"type": "string"},
                "refreshToken": {"type": "string"},
                "user": {
                    "type": "object",
                    "required": [
                        "email",
                        "name"
                    ],
                    "properties": {
                        "email": {"type": "string", "const": self.email},
                        "name": {"type": "string", "const": self.name}
                    }
                }
            }
        }
