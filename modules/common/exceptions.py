from http import HTTPStatus


class BaseHttpException(Exception):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    detail = "Internal server error"


class ObjectDoesNotExist(BaseHttpException):
    status_code = HTTPStatus.NOT_FOUND
    detail = "Object does not exist"


class ObjectAlreadyExists(BaseHttpException):
    status_code = HTTPStatus.CONFLICT
    detail = "Object already exists"


class PermissionDenied(BaseHttpException):
    status_code = HTTPStatus.FORBIDDEN
    detail = "Permission denied"
