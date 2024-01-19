from typing import Annotated

from fastapi import Depends

from backend.config.oauth2 import oauth2_scheme
from backend.dependencies.auth.creators import get_token_service
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.auth.services import (
    TokenService,
)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
) -> CurrentUserData:
    return token_service.decode(token)
