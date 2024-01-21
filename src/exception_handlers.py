from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from api.v1.common.exceptions import DateRangeConflict
from backend.src.core.modules.auth.exceptions import InvalidCredentials
from backend.src.core.modules.common.exceptions import (
    BaseHttpException,
    ObjectDoesNotExist,
    ObjectAlreadyExists,
    PermissionDenied,
)
from backend.src.core.modules.user.exceptions import PasswordDoesNotMatch


# pylint: disable=W0613
async def http_exception_handler(request: Request, exception: BaseHttpException):
    if isinstance(exception, PasswordDoesNotMatch):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exception.detail},
        )

    if isinstance(exception, InvalidCredentials):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exception.detail},
        )

    if isinstance(exception, ObjectDoesNotExist):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": exception.detail}
        )

    if isinstance(exception, ObjectAlreadyExists):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content={"detail": exception.detail}
        )

    if isinstance(exception, PermissionDenied):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN, content={"detail": exception.detail}
        )

    if isinstance(exception, DateRangeConflict):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=exception.detail
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Unknown error"},
    )
