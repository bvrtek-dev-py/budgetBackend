from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi import status

from backend.api.v1.common.responses import ErrorResponse
from backend.api.v1.transaction.requests import (
    TransactionUpdateRequest,
)
from backend.api.v1.transaction.responses.transaction import TransactionBaseResponse
from backend.modules.subject.dependencies import (
    subject_owner_permission,
)
from backend.modules.transaction.dependencies import (
    get_transaction_service,
    transaction_owner_permission,
)
from backend.modules.transaction.schemas import (
    TransactionUpdateDTO,
)
from backend.modules.transaction.services.crud_service import TransactionService

router = APIRouter(prefix="/api/v1/transactions", tags=["APIv1 Transaction"])


@router.put(
    "/{transaction_id}",
    responses={
        200: {"model": TransactionBaseResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
    response_model=TransactionBaseResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(transaction_owner_permission),
        Depends(subject_owner_permission),
    ],
)
async def update_transaction(
    transaction_id: Annotated[int, Path(gt=0)],
    request: TransactionUpdateRequest,
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
):
    return await transaction_service.update(
        transaction_id, TransactionUpdateDTO(**request.model_dump())
    )


@router.get(
    "/{transaction_id}",
    responses={
        200: {"model": TransactionBaseResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    response_model=TransactionBaseResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(transaction_owner_permission)],
)
async def get_transaction(
    transaction_id: Annotated[int, Path(gt=0)],
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
):
    return await transaction_service.get_by_id(transaction_id)


@router.delete(
    "/{transaction_id}",
    responses={
        204: {},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(transaction_owner_permission)],
)
async def delete_transaction(
    transaction_id: Annotated[int, Path(gt=0)],
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
):
    return await transaction_service.delete(transaction_id)
