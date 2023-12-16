from fastapi import HTTPException
from starlette import status

ObjectDoesNotExist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Object does not exist"
)


ObjectAlreadyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Object already exists"
)


PermissionDenied = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
)
