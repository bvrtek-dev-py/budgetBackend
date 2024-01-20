from http import HTTPStatus

from backend.src.core.modules.common.exceptions import BaseHttpException


class PasswordDoesNotMatch(BaseHttpException):
    status_code = HTTPStatus.CONFLICT
    detail = "Passwords does not match"
