from fastapi import HTTPException
from starlette import status

ObjectDoesNotExist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Object does not exist"
)
