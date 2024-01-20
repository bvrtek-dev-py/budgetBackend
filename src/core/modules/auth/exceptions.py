from http import HTTPStatus

from backend.src.core.modules.common.exceptions import BaseHttpException


class InvalidCredentials(BaseHttpException):
    status_code = HTTPStatus.NOT_FOUND
    detail = "Invalid login data"
