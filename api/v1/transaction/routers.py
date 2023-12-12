from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from fastapi import status

from backend.api.v1.common.responses import ErrorResponse
from backend.api.v1.transaction.requests import (
    TransactionCreateRequest,
    TransactionUpdateRequest,
)
from backend.api.v1.transaction.responses import TransactionBaseResponse
from backend.modules.transaction.dependencies import get_transaction_service
from backend.modules.transaction.services import TransactionService

router = APIRouter(prefix="/api/v1/transactions", tags=["APIv1 Transactions"])


@router.post(
    "/",
    responses={201: {"model": TransactionBaseResponse}, 422: {"model": ErrorResponse}},
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
    request: TransactionCreateRequest,
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
):
    return await transaction_service.create(
        request.name, request.value, request.type, request.description
    )


@router.put(
    "/{transaction_id}",
    responses={
        200: {"model": TransactionBaseResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
)
async def update_transaction(
    transaction_id: Annotated[int, Path(gt=0)],
    request: TransactionUpdateRequest,
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
):
    return await transaction_service.update(
        transaction_id, request.name, request.value, request.description
    )


@router.get(
    "/{transaction_id}",
    responses={
        200: {"model": TransactionBaseResponse},
        404: {"model": ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
)
async def get_transaction(
    transaction_id: Annotated[int, Path(gt=0)],
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
):
    return await transaction_service.get_by_id(transaction_id)


@router.get(
    "/", response_model=List[TransactionBaseResponse], status_code=status.HTTP_200_OK
)
async def get_transactions(
    transaction_service: Annotated[TransactionService, Depends(get_transaction_service)]
):
    return await transaction_service.get_all()


@router.delete(
    "/{transaction_id}",
    responses={
        204: {},
        404: {"model": ErrorResponse},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_transaction(
    transaction_id: Annotated[int, Path(gt=0)],
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
):
    return await transaction_service.delete(transaction_id)
