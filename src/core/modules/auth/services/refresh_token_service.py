from backend.src.core.modules.auth.schemas import (
    AuthenticatedUserDTO,
    SuccessAuthenticationDTO,
)
from backend.src.core.modules.auth.services.token_service import TokenService


class RefreshTokenService:
    def __init__(self, token_service: TokenService):
        self._token_service = token_service

    def refresh(self, token: str) -> SuccessAuthenticationDTO:
        decoded_data = self._token_service.decode(token)
        token_data = AuthenticatedUserDTO(id=decoded_data.id, sub=decoded_data.email)

        return SuccessAuthenticationDTO(
            token_type="Bearer",
            access_token=self._token_service.create_access_token(token_data),
            refresh_token=self._token_service.create_refresh_token(token_data),
            expired_at=self._token_service.get_expire_token_datetime(),
        )
