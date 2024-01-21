from typing import List, Annotated

from fastapi import APIRouter, status, Depends, Path

from api.v1.common.query_parameters import DateRangeParameters
from backend.src.api.v1.common.responses import ErrorResponse
from backend.src.api.v1.transaction.responses.transaction import TransactionBaseResponse
from backend.src.core.modules.transaction.services.query_service import (
    TransactionQueryService,
)
from backend.src.dependencies.subject.permissions import SubjectOwnerPermission
from backend.src.dependencies.transaction.creators import get_transaction_query_service

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
    transaction_query_service: Annotated[
        TransactionQueryService, Depends(get_transaction_query_service)
    ],
    date_range: DateRangeParameters,
):
    return await transaction_query_service.get_subject_transactions(
        subject_id, date_range.start_date, date_range.end_date
    )
