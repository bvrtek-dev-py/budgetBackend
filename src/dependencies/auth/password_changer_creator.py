from typing import Annotated

from fastapi import Depends

from backend.src.core.modules.auth.services.password_services import (
    PasswordChangeService,
)
from backend.src.core.modules.auth.services.password_services import (
    PasswordHashService,
    PasswordVerifyService,
)
from backend.src.core.modules.user.interfaces import UserRepositoryInterface
from backend.src.core.modules.user.use_cases import UserRetrievalUseCase
from backend.src.dependencies.auth.creators import (
    get_password_hash_service,
    get_password_verify_service,
)
from backend.src.dependencies.user.creators import (
    get_user_retrieval_use_case,
    get_user_repository,
)


def get_password_change_service(
    retrieval_use_case: Annotated[
        UserRetrievalUseCase, Depends(get_user_retrieval_use_case)
    ],
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
    hash_service: Annotated[PasswordHashService, Depends(get_password_hash_service)],
    verify_service: Annotated[
        PasswordVerifyService, Depends(get_password_verify_service)
    ],
) -> PasswordChangeService:
    return PasswordChangeService(
        user_repository=user_repository,
        retrieval_use_case=retrieval_use_case,
        hash_service=hash_service,
        verify_service=verify_service,
    )
