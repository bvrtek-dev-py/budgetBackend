from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from fastapi import status

from budgetBackend.api.v1.common.responses import ErrorResponse
from budgetBackend.api.v1.subject.requests import (
    SubjectCreateRequest,
    SubjectUpdateRequest,
)
from budgetBackend.api.v1.subject.responses import SubjectBaseResponse
from budgetBackend.modules.subject.dependencies import get_subject_service
from budgetBackend.modules.subject.services import SubjectService

router = APIRouter(prefix="/api/v1/subjects", tags=["APIv1 Subject"])


@router.post(
    "/",
    responses={201: {"model": SubjectBaseResponse}, 422: {"model": ErrorResponse}},
    status_code=status.HTTP_201_CREATED,
)
async def create_subject(
    request: SubjectCreateRequest,
    subject_service: Annotated[SubjectService, Depends(get_subject_service)],
):
    return await subject_service.create(request.name)


@router.put(
    "/{subject_id}",
    responses={
        200: {"model": SubjectBaseResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
)
async def update_subject(
    subject_id: Annotated[int, Path(gt=0)],
    request: SubjectUpdateRequest,
    subject_service: Annotated[SubjectService, Depends(get_subject_service)],
):
    return await subject_service.update(subject_id, request.name)


@router.get(
    "/{subject_id}",
    responses={
        200: {"model": SubjectBaseResponse},
        404: {"model": ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
)
async def get_subject(
    subject_id: int,
    subject_service: Annotated[SubjectService, Depends(get_subject_service)],
):
    return await subject_service.get_by_id(subject_id)


@router.get(
    "/", response_model=List[SubjectBaseResponse], status_code=status.HTTP_200_OK
)
async def get_subjects(
    subject_service: Annotated[SubjectService, Depends(get_subject_service)]
):
    return await subject_service.get_all()


@router.delete(
    "/{subject_id}",
    responses={
        204: {},
        404: {"model": ErrorResponse},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_subject(
    subject_id: int,
    subject_service: Annotated[SubjectService, Depends(get_subject_service)],
):
    return await subject_service.delete(subject_id)
