from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Path
from fastapi import status

from backend.api.v1.category.requests import (
    CategoryCreateRequest,
    CategoryUpdateRequest,
)
from backend.api.v1.category.responses import CategoryBaseResponse, CategoryGetResponse
from backend.api.v1.common.responses import ErrorResponse
from backend.modules.auth.dependencies import get_current_user
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.category.dependencies import (
    get_category_service,
    category_owner_permission,
)
from backend.modules.category.services import CategoryService
from backend.modules.transaction.enums import TransactionType

router = APIRouter(prefix="/api/v1/categories", tags=["APIv1 Category"])


@router.post(
    "/",
    responses={
        201: {"model": CategoryBaseResponse},
        401: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryBaseResponse,
)
async def create_category(
    request: CategoryCreateRequest,
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    return await category_service.create(
        current_user.id,
        request.name,
        request.transaction_type,
    )


@router.put(
    "/{category_id}",
    responses={
        200: {"model": CategoryBaseResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=CategoryBaseResponse,
    dependencies=[Depends(category_owner_permission)],
)
async def update_category(
    category_id: Annotated[int, Path(gt=0)],
    request: CategoryUpdateRequest,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    return await category_service.update(category_id, request.name)


@router.get(
    "/{category_id}",
    responses={
        200: {"model": CategoryGetResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=CategoryGetResponse,
    dependencies=[Depends(category_owner_permission)],
)
async def get_category(
    category_id: int,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    return await category_service.get_by_id(category_id)


@router.get(
    "/",
    responses={
        200: {"model": List[CategoryGetResponse]},
        401: {"model": ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=List[CategoryGetResponse],
)
async def get_user_categories(
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
    transaction_type: Optional[TransactionType] = None,
):
    return await category_service.get_by_user_id(current_user.id, transaction_type)


@router.delete(
    "/{category_id}",
    responses={
        204: {},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(category_owner_permission)],
)
async def delete_category(
    category_id: int,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    return await category_service.delete(category_id)
