from http import HTTPStatus

from backend.src.core.modules.common.exceptions import BaseHttpException


class DateRangeConflict(BaseHttpException):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    detail = "End date must be greater than or equal to start date"
