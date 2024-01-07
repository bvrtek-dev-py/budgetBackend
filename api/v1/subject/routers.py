from datetime import date
from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Path
from fastapi import status

from backend.api.v1.common.responses import ErrorResponse
from backend.api.v1.common.validators import validate_date_range
from backend.api.v1.subject.requests import (
    SubjectRequest,
)
from backend.api.v1.subject.responses import SubjectBaseResponse, SubjectGetResponse
from backend.api.v1.transaction.responses.transaction import TransactionBaseResponse
from backend.modules.auth.dependencies import get_current_user
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.subject.dependencies import (
    get_subject_service,
    subject_owner_permission,
)
from backend.modules.subject.services import SubjectService
from backend.modules.transaction.dependencies import (
    get_transaction_query_service,
)
from backend.modules.transaction.services.query_service import TransactionQueryService

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


@router.get(
    "/{subject_id}/transactions",
    responses={
        200: {"model": List[TransactionBaseResponse]},
        401: {"model": ErrorResponse},
    },
    response_model=List[TransactionBaseResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(subject_owner_permission)],
)
async def get_subject_transactions(
    subject_id: Annotated[int, Path(gt=0)],
    subject_service: Annotated[SubjectService, Depends(get_subject_service)],
    transaction_query_service: Annotated[
        TransactionQueryService, Depends(get_transaction_query_service)
    ],
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    if start_date is not None and end_date is not None:
        validate_date_range(start_date, end_date)

    subject = await subject_service.get_by_id(subject_id)

    return await transaction_query_service.get_subject_transactions(
        subject, start_date, end_date
    )
