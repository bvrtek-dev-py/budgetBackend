from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from fastapi import status

from budgetBackend.api.v1.category.requests import (
    CategoryCreateRequest,
    CategoryUpdateRequest,
)
from budgetBackend.api.v1.category.responses import CategoryBaseResponse
from budgetBackend.api.v1.common.responses import ErrorResponse
from budgetBackend.modules.category.dependencies import get_category_service
from budgetBackend.modules.category.services import CategoryService

router = APIRouter(prefix="/api/v1/categories", tags=["API v1", "Category"])


@router.post(
    "/",
    responses={201: {"model": CategoryBaseResponse}, 422: {"model": ErrorResponse}},
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    request: CategoryCreateRequest,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    return await category_service.create(
        request.name,
        request.type,
    )


@router.put(
    "/{category_id}",
    responses={
        200: {"model": CategoryBaseResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
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
        200: {"model": CategoryBaseResponse},
        404: {"model": ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
)
async def get_category(
    category_id: int,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    return await category_service.get_by_id(category_id)


@router.get(
    "/", response_model=List[CategoryBaseResponse], status_code=status.HTTP_200_OK
)
async def get_categories(
    category_service: Annotated[CategoryService, Depends(get_category_service)]
):
    return await category_service.get_all()


@router.delete(
    "/{category_id}",
    responses={
        204: {},
        404: {"model": ErrorResponse},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(
    category_id: int,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    return await category_service.delete(category_id)
