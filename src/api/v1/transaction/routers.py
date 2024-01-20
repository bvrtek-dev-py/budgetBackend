from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi import status

from backend.src.api.v1.common.responses import ErrorResponse
from backend.src.api.v1.transaction.requests.transaction import (
    TransactionUpdateRequest,
)
from backend.src.api.v1.transaction.responses.transaction import TransactionBaseResponse
from backend.src.dependencies.category.permissions import CategoryOwnerPermission
from backend.src.dependencies.common.enums import IdentifierSource
from backend.src.dependencies.subject.permissions import SubjectOwnerPermission
from backend.src.dependencies.transaction.creators import (
    get_transaction_service,
)
from backend.src.dependencies.transaction.permissions import (
    TransactionOwnerPermission,
)
from backend.src.core.modules.transaction.schemas.transaction import (
    TransactionUpdateDTO,
)
from backend.src.core.modules.transaction.services.crud_service import (
    TransactionService,
)

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
        Depends(TransactionOwnerPermission()),
        Depends(SubjectOwnerPermission(source=IdentifierSource.REQUEST_BODY)),
        Depends(CategoryOwnerPermission(source=IdentifierSource.REQUEST_BODY)),
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
    dependencies=[Depends(TransactionOwnerPermission())],
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
    dependencies=[Depends(TransactionOwnerPermission())],
)
async def delete_transaction(
    transaction_id: Annotated[int, Path(gt=0)],
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
):
    return await transaction_service.delete(transaction_id)
