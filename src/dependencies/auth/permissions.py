from typing import Annotated

from fastapi import Depends

from backend.src.config.oauth2 import oauth2_scheme
from backend.src.dependencies.auth.creators import get_token_service
from backend.src.core.modules.auth.schemas import CurrentUserData
from backend.src.core.modules.auth.services.token_service import (
    TokenService,
)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
) -> CurrentUserData:
    return token_service.decode(token)
