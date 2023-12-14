from fastapi import HTTPException
from starlette import status


InvalidCredentials = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Invalid login data"
)
