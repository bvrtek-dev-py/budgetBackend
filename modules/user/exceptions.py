from fastapi.exceptions import HTTPException
from fastapi import status


PasswordDoesNotMatch = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Passwords does not match"
)
