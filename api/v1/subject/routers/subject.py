from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi import status

from backend.api.v1.common.responses import ErrorResponse
from backend.api.v1.subject.requests import (
    SubjectRequest,
)
from backend.api.v1.subject.responses import SubjectBaseResponse, SubjectGetResponse
from backend.modules.auth.dependencies import get_current_user
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.subject.dependencies import (
    get_subject_service,
    subject_owner_permission,
)
from backend.modules.subject.services import SubjectService

router = APIRouter(prefix="/api/v1/subjects", tags=["APIv1 Subject"])


@router.post(
    "/",
    responses={
        201: {"model": SubjectBaseResponse},
        401: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
    response_model=SubjectBaseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_subject(
    request: SubjectRequest,
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    subject_service: Annotated[SubjectService, Depends(get_subject_service)],
):
    return await subject_service.create(request.name, current_user.id)


@router.put(
    "/{subject_id}",
    responses={
        200: {"model": SubjectBaseResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
    response_model=SubjectBaseResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(subject_owner_permission)],
)
async def update_subject(
    subject_id: Annotated[int, Path(gt=0)],
    request: SubjectRequest,
    subject_service: Annotated[SubjectService, Depends(get_subject_service)],
):
    return await subject_service.update(subject_id, request.name)


@router.get(
    "/{subject_id}",
    responses={
        200: {"model": SubjectBaseResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    response_model=SubjectGetResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(subject_owner_permission)],
)
async def get_subject(
    subject_id: Annotated[int, Path(gt=0)],
    subject_service: Annotated[SubjectService, Depends(get_subject_service)],
):
    return await subject_service.get_by_id(subject_id)


@router.delete(
    "/{subject_id}",
    responses={
        204: {},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(subject_owner_permission)],
)
async def delete_subject(
    subject_id: Annotated[int, Path(gt=0)],
    subject_service: Annotated[SubjectService, Depends(get_subject_service)],
):
    return await subject_service.delete(subject_id)
