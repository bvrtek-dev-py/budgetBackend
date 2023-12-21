from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from fastapi import status

from backend.api.v1.common.responses import ErrorResponse
from backend.api.v1.subject.requests import (
    SubjectRequest,
)
from backend.api.v1.subject.responses import SubjectBaseResponse, SubjectGetResponse
from backend.modules.auth.dependencies import get_current_user
from backend.modules.subject.dependencies import (
    get_subject_service,
    subject_owner_permission,
)
from backend.modules.subject.services import SubjectService
from backend.modules.user.dependencies import get_user_service
from backend.modules.user.services import UserService

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
    current_user_email: Annotated[str, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    subject_service: Annotated[SubjectService, Depends(get_subject_service)],
):
    user = await user_service.get_by_email(current_user_email)
    return await subject_service.create(request.name, user.id)


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


@router.get(
    "/",
    responses={
        200: {"model": List[SubjectBaseResponse]},
        401: {"model": ErrorResponse},
    },
    response_model=List[SubjectBaseResponse],
    status_code=status.HTTP_200_OK,
)
async def get_user_subjects(
    current_user_email: Annotated[str, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    subject_service: Annotated[SubjectService, Depends(get_subject_service)],
):
    user = await user_service.get_by_email(current_user_email)
    return await subject_service.get_by_user_id(user.id)


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
