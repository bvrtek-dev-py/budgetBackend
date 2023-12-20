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
from backend.modules.category.dependencies import (
    get_category_service,
    category_owner_permission,
)
from backend.modules.category.services import CategoryService
from backend.modules.transaction.enums import TransactionType
from backend.modules.user.dependencies import get_user_service
from backend.modules.user.services import UserService

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
    current_user_email: Annotated[str, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    user = await user_service.get_by_email(current_user_email)
    return await category_service.create(
        user.id,
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
    current_user_email: Annotated[str, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
    transaction_type: Optional[TransactionType] = None,
):
    user = await user_service.get_by_email(current_user_email)
    return await category_service.get_by_user_id(user.id, transaction_type)


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
