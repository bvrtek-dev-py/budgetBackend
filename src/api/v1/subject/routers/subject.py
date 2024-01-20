from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi import status

from backend.src.api.v1.common.responses import ErrorResponse
from backend.src.api.v1.subject.requests import (
    SubjectRequest,
)
from backend.src.api.v1.subject.responses import SubjectBaseResponse, SubjectGetResponse
from backend.src.dependencies.auth.permissions import get_current_user
from backend.src.dependencies.subject.dependencies import (
    get_subject_service,
)
from backend.src.dependencies.subject.permissions import SubjectOwnerPermission
from backend.src.core.modules.auth.schemas import CurrentUserData
from backend.src.core.modules.subject.schemas import SubjectPayloadDTO
from backend.src.core.modules.subject.services import SubjectService

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
    return await subject_service.create(
        SubjectPayloadDTO(**request.model_dump()), current_user.id
    )


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
    dependencies=[Depends(SubjectOwnerPermission())],
)
async def update_subject(
    subject_id: Annotated[int, Path(gt=0)],
    request: SubjectRequest,
    subject_service: Annotated[SubjectService, Depends(get_subject_service)],
):
    return await subject_service.update(
        subject_id, SubjectPayloadDTO(**request.model_dump())
    )


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
    dependencies=[Depends(SubjectOwnerPermission())],
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
    dependencies=[Depends(SubjectOwnerPermission())],
)
async def delete_subject(
    subject_id: Annotated[int, Path(gt=0)],
    subject_service: Annotated[SubjectService, Depends(get_subject_service)],
):
    return await subject_service.delete(subject_id)
