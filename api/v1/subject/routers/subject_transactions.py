from datetime import date
from typing import List, Annotated, Optional

from fastapi import APIRouter, status, Depends, Path

from backend.api.v1.common.responses import ErrorResponse
from backend.api.v1.common.validators import validate_date_range
from backend.api.v1.transaction.responses.transaction import TransactionBaseResponse
from backend.dependencies.subject.dependencies import (
    get_subject_service,
)
from backend.dependencies.subject.permissions import SubjectOwnerPermission
from backend.dependencies.transaction.creators import get_transaction_query_service
from backend.modules.subject.services import SubjectService
from backend.modules.transaction.services.query_service import TransactionQueryService

router = APIRouter(
    prefix="/api/v1/subjects/{subject_id}/transactions",
    tags=["APIv1 Subject Transactions"],
)


@router.get(
    "/",
    responses={
        200: {"model": List[TransactionBaseResponse]},
        401: {"model": ErrorResponse},
    },
    response_model=List[TransactionBaseResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(SubjectOwnerPermission())],
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
